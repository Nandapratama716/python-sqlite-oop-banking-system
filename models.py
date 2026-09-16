"""
Project: SQLite + Python OOP Based Banking System 

Author  : Creative Online School
License : Apache 2.0
URL     : https://creativeonlineschool.com
"""

class Customer:
    def __init__(self, customer_id, name):
        self.customer_id = customer_id
        self.name = name


class Account:
    def __init__(self, account_number, customer_id, balance=0.0):
        self.account_number = account_number
        self.customer_id = customer_id
        self.balance = balance

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Invalid deposit amount")
        self.balance += amount

    def withdraw(self, amount):
        raise NotImplementedError


class SavingsAccount(Account):
    def withdraw(self, amount):
        if amount > self.balance:
            raise ValueError("Insufficient funds")
        self.balance -= amount


class CurrentAccount(Account):
    def __init__(self, account_number, customer_id, balance=0.0, overdraft=500):
        super().__init__(account_number, customer_id, balance)
        self.overdraft = overdraft

    def withdraw(self, amount):
        if amount > self.balance + self.overdraft:
            raise ValueError("Overdraft limit exceeded")
        self.balance -= amount
