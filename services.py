"""
Project: SQLite + Python OOP Based Banking System 

Author  : Creative Online School
License : Apache 2.0
URL     : https://creativeonlineschool.com
"""

class BankingService:
    def __init__(self, account_repo, tx_repo):
        self.account_repo = account_repo
        self.tx_repo = tx_repo

    def deposit(self, account, amount):
        account.deposit(amount)
        self.account_repo.update_balance(account)
        self.tx_repo.log(account.account_number, amount, "DEPOSIT")

    def withdraw(self, account, amount):
        account.withdraw(amount)
        self.account_repo.update_balance(account)
        self.tx_repo.log(account.account_number, amount, "WITHDRAW")
