"""
Project: SQLite + Python OOP Based Banking System 

Author  : Creative Online School
License : Apache 2.0
URL     : https://creativeonlineschool.com
"""

from database import Database
from models import SavingsAccount
from repositories import AccountRepository, TransactionRepository
from services import BankingService

db = Database()
account_repo = AccountRepository(db)
tx_repo = TransactionRepository(db)
service = BankingService(account_repo, tx_repo)

# Example usage
account = SavingsAccount("ACC1001", 1, 1000)
service.deposit(account, 500)
service.withdraw(account, 200)
print("Final Balance:", account.balance)
