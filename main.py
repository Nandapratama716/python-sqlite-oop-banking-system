"""
Project: SQLite + Python OOP Based Banking System

Author  : Creative Online School
License : Apache 2.0
URL     : https://creativeonlineschool.com
"""

from database import Database
from models import SavingsAccount, CurrentAccount
from repositories import (
    CustomerRepository,
    AccountRepository,
    TransactionRepository,
)
from services import BankingService


def setup_application():
    """
    Initialize the database, repositories, banking service,
    customer, and bank accounts.
    """

    db = Database()
    db.initialize()

    customer_repo = CustomerRepository(db)
    account_repo = AccountRepository(db)
    transaction_repo = TransactionRepository(db)

    service = BankingService(
        account_repo,
        transaction_repo,
    )

    customer_id = customer_repo.get_or_create("Jon")

    savings_account = load_or_create_savings_account(
        account_repo,
        customer_id,
    )

    current_account = load_or_create_current_account(
        account_repo,
        customer_id,
    )

    accounts = {
        savings_account.account_number: savings_account,
        current_account.account_number: current_account,
    }

    return accounts, service, transaction_repo


def load_or_create_savings_account(account_repo, customer_id):
    """Load an existing savings account or create a new one."""

    account_number = "ACC1001"

    existing_account = account_repo.find_by_account_number(
        account_number
    )

    if existing_account:
        return SavingsAccount(
            existing_account[0],
            existing_account[1],
            existing_account[2],
        )

    account = SavingsAccount(
        account_number,
        customer_id,
        1000,
    )

    account_repo.create(
        account,
        "Savings",
    )

    return account


def load_or_create_current_account(account_repo, customer_id):
    """Load an existing current account or create a new one."""

    account_number = "ACC2001"

    existing_account = account_repo.find_by_account_number(
        account_number
    )

    if existing_account:
        return CurrentAccount(
            existing_account[0],
            existing_account[1],
            existing_account[2],
            overdraft=500,
        )

    account = CurrentAccount(
        account_number,
        customer_id,
        1000,
        overdraft=500,
    )

    account_repo.create(
        account,
        "Current",
    )

    return account


def show_menu():
    """Display the banking system menu."""

    print("\n===== PYTHON BANKING SYSTEM =====")
    print("1. Check Balance")
    print("2. Deposit")
    print("3. Withdraw")
    print("4. Transfer")
    print("5. Transaction History")
    print("0. Exit")


def check_balance(accounts):
    """Display the balance of an account."""

    account_number = input("Account number: ")
    account = accounts.get(account_number)

    if not account:
        print("Account not found.")
        return

    print("Balance:", account.balance)


def deposit(accounts, service):
    """Deposit money into an account."""

    account_number = input("Account number: ")
    account = accounts.get(account_number)

    if not account:
        print("Account not found.")
        return

    amount = float(input("Deposit amount: "))

    service.deposit(
        account,
        amount,
    )

    print("Deposit successful.")
    print("New balance:", account.balance)


def withdraw(accounts, service):
    """Withdraw money from an account."""

    account_number = input("Account number: ")
    account = accounts.get(account_number)

    if not account:
        print("Account not found.")
        return

    amount = float(input("Withdraw amount: "))

    service.withdraw(
        account,
        amount,
    )

    print("Withdraw successful.")
    print("New balance:", account.balance)


def transfer(accounts, service):
    """Transfer money between two accounts."""

    from_number = input("From account: ")
    to_number = input("To account: ")

    from_account = accounts.get(from_number)
    to_account = accounts.get(to_number)

    if not from_account or not to_account:
        print("Account not found.")
        return

    if from_number == to_number:
        print("Cannot transfer to the same account.")
        return

    amount = float(input("Transfer amount: "))

    service.transfer(
        from_account,
        to_account,
        amount,
    )

    print("Transfer successful.")
    print("Sender balance:", from_account.balance)
    print("Receiver balance:", to_account.balance)


def show_transaction_history(accounts, transaction_repo):
    """Display transaction history for an account."""

    account_number = input("Account number: ")

    if account_number not in accounts:
        print("Account not found.")
        return

    transactions = transaction_repo.find_by_account_number(
        account_number
    )

    if not transactions:
        print("No transactions found.")
        return

    print("\n===== TRANSACTION HISTORY =====")

    for transaction in transactions:
        transaction_type = transaction[3]
        amount = transaction[2]
        timestamp = transaction[4]

        print(
            f"{transaction_type} | "
            f"{amount} | "
            f"{timestamp}"
        )


def main():
    """Run the banking system CLI."""

    accounts, service, transaction_repo = setup_application()

    while True:
        show_menu()

        choice = input("Choose option: ")

        try:
            if choice == "1":
                check_balance(accounts)

            elif choice == "2":
                deposit(
                    accounts,
                    service,
                )

            elif choice == "3":
                withdraw(
                    accounts,
                    service,
                )

            elif choice == "4":
                transfer(
                    accounts,
                    service,
                )

            elif choice == "5":
                show_transaction_history(
                    accounts,
                    transaction_repo,
                )

            elif choice == "0":
                print(
                    "Thank you for using the banking system."
                )
                break

            else:
                print("Invalid option.")

        except ValueError as error:
            print("Error:", error)


if __name__ == "__main__":
    main()