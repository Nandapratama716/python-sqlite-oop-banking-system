"""
Project: SQLite + Python OOP Based Banking System 

Author  : Creative Online School
License : Apache 2.0
URL     : https://creativeonlineschool.com
"""

from datetime import datetime

class CustomerRepository:
    def __init__(self, db):
        self.db = db

    def create(self, name):
        return self.db.execute("INSERT INTO customers (name) VALUES (?)", (name,))

    def find_by_name(self, name):
        return self.db.fetchone(
            "SELECT id, name FROM customers WHERE name=?",
            (name,)
        )

    def get_or_create(self, name):
        customer = self.find_by_name(name)

        if customer:
            return customer[0]

        return self.create(name)

class AccountRepository:
    def __init__(self, db):
        self.db = db

    def create(self, account, account_type):
        self.db.execute(
            """
            INSERT INTO accounts
            (account_number, customer_id, balance, type)
            VALUES (?, ?, ?, ?)
            """,
            (
                account.account_number,
                account.customer_id,
                account.balance,
                account_type
            )
        )

    def find_by_account_number(self, account_number):
        return self.db.fetchone(
            """
            SELECT account_number, customer_id, balance, type
            FROM accounts
            WHERE account_number=?
            """,
            (account_number,)
        )

    def update_balance(self, account):
        self.db.execute(
            "UPDATE accounts SET balance=? WHERE account_number=?",
            (account.balance, account.account_number)
        )


class TransactionRepository:
    def __init__(self, db):
        self.db = db

    def log(self, account_number, amount, tx_type):
        self.db.execute(
            "INSERT INTO transactions (account_number, amount, transaction_type, timestamp) VALUES (?, ?, ?, ?)",
            (account_number, amount, tx_type, datetime.now().isoformat())
        )

    def find_by_account_number(self, account_number):
        return self.db.fetchall(
            """
            SELECT id, account_number, amount, transaction_type, timestamp
            FROM transactions
            WHERE account_number=?
            ORDER BY id
            """,
            (account_number,)
        )
