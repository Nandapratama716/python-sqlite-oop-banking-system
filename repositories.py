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
        self.db.execute("INSERT INTO customers (name) VALUES (?)", (name,))


class AccountRepository:
    def __init__(self, db):
        self.db = db

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
