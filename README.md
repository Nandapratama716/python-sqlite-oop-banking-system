# Python SQLite OOP Banking System

A simple command-line banking system built with **Python**, **SQLite**, and **Object-Oriented Programming (OOP)**.

This project is part of my **Full Stack AI Engineer learning journey** and was developed to practice Python fundamentals, OOP concepts, database persistence, repository patterns, service-layer architecture, validation, and clean separation of responsibilities.

> This project is intended for educational purposes and is not a production banking application.

---

## 📌 Project Overview

The application simulates a simple banking system where a customer can manage different types of bank accounts through a command-line interface.

The system supports:

- Savings Account
- Current Account
- Persistent SQLite storage
- Deposits
- Withdrawals
- Fund transfers
- Transaction history
- Overdraft limits
- Account validation

Unlike a basic in-memory Python program, account balances and transaction history are stored in SQLite so the data remains available after the application is closed and restarted.

---

## ✨ Features

### Customer Management

The application creates or retrieves an existing customer from the database.

This prevents duplicate customer records when the application is restarted.

---

### Savings Account

Savings accounts support:

- Balance checking
- Deposits
- Withdrawals
- Fund transfers
- Transaction history

A Savings Account cannot withdraw more money than the available balance.

Example:

```text
Balance: 1000
Withdraw: 1500

Result:
Insufficient funds
```

---

### Current Account

Current accounts support the same banking operations but include an **overdraft limit**.

Example:

```text
Balance: 1000
Overdraft Limit: 500

Maximum available amount: 1500
```

A withdrawal of:

```text
1300
```

is allowed.

The resulting balance becomes:

```text
-300
```

However, attempting to withdraw beyond the overdraft limit will produce:

```text
Overdraft limit exceeded
```

---

### Deposit

Users can deposit money into an account.

Example:

```text
Current Balance: 1000
Deposit: 500
New Balance: 1500
```

Each successful deposit is stored in the transaction history.

---

### Withdraw

Users can withdraw money from an account.

The withdrawal behavior depends on the account type.

Savings Account:

```text
Cannot withdraw more than the available balance.
```

Current Account:

```text
Can withdraw beyond the current balance within the overdraft limit.
```

---

### Fund Transfer

Money can be transferred between available accounts.

Example:

```text
From:
ACC1001

To:
ACC2001

Amount:
300
```

The application:

```text
1. Withdraws 300 from ACC1001
2. Deposits 300 into ACC2001
3. Updates both account balances
4. Records TRANSFER_OUT
5. Records TRANSFER_IN
```

The system also prevents transfers to the same account.

---

### Transaction History

Every successful financial operation is recorded in SQLite.

Transaction types include:

```text
DEPOSIT
WITHDRAW
TRANSFER_OUT
TRANSFER_IN
```

Each transaction contains:

```text
Account Number
Amount
Transaction Type
Timestamp
```

Users can view transaction history directly from the CLI.

---

### Persistent Data

Account balances and transaction history are stored inside SQLite.

This means:

```text
Run application
↓
Perform transaction
↓
Close application
↓
Run application again
↓
Previous balance is still available
```

The application loads an existing account instead of creating duplicate records.

---

## 🧰 Tech Stack

| Technology | Purpose |
|---|---|
| Python 3 | Core programming language |
| SQLite | Relational database |
| sqlite3 | Python SQLite interface |
| OOP | Application/domain modeling |
| SQL | Data storage and retrieval |
| CLI | User interaction |

The project currently uses only Python standard-library modules, so no external Python dependencies are required.

---

## 🏗️ Application Architecture

The project separates responsibilities into multiple layers:

```text
┌─────────────────────────────┐
│      CLI / Presentation     │
│          main.py            │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│       Service Layer         │
│        services.py          │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│        Domain Layer         │
│         models.py           │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│      Repository Layer       │
│      repositories.py        │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│       Database Layer        │
│ database.py + schema.sql    │
└──────────────┬──────────────┘
               │
               ▼
          SQLite Database
             bank.db
```

This separation makes the project easier to understand, maintain, test, and extend.

---

## 📂 Project Structure

```text
python-sqlite-oop-banking-system/
│
├── database.py
├── main.py
├── models.py
├── repositories.py
├── services.py
├── schema.sql
├── README.md
└── .gitignore
```

### `main.py`

The application entry point.

Responsibilities:

```text
Initialize the application
Load/create customer
Load/create accounts
Display CLI menu
Handle user interaction
```

---

### `database.py`

Handles SQLite database operations.

Responsibilities:

```text
Database connection
SQL execution
Fetch one record
Fetch multiple records
Database schema initialization
```

The database is automatically initialized using:

```text
schema.sql
```

---

### `models.py`

Contains the application's domain models and OOP logic.

Main classes:

```text
Customer
Account
SavingsAccount
CurrentAccount
```

The `Account` class acts as the base account model.

`SavingsAccount` and `CurrentAccount` inherit from `Account`.

---

### `repositories.py`

Handles communication between the application and SQLite.

Repositories include:

```text
CustomerRepository
AccountRepository
TransactionRepository
```

The repository layer keeps SQL queries separate from the main business logic.

---

### `services.py`

Contains banking business logic.

Main operations:

```text
Deposit
Withdraw
Transfer
```

The service layer coordinates domain models and repositories.

---

### `schema.sql`

Defines the SQLite database structure.

The project uses three main tables:

```text
customers
accounts
transactions
```

---

## 🗄️ Database Design

### Customers Table

Stores customer information.

```sql
CREATE TABLE IF NOT EXISTS customers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
);
```

---

### Accounts Table

Stores bank account information.

```sql
CREATE TABLE IF NOT EXISTS accounts (
    account_number TEXT PRIMARY KEY,
    customer_id INTEGER,
    balance REAL DEFAULT 0,
    type TEXT,
    FOREIGN KEY(customer_id) REFERENCES customers(id)
);
```

Main fields:

| Field | Description |
|---|---|
| account_number | Unique account number |
| customer_id | Owner of the account |
| balance | Current account balance |
| type | Savings or Current |

---

### Transactions Table

Stores transaction history.

```sql
CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    account_number TEXT,
    amount REAL,
    transaction_type TEXT,
    timestamp TEXT
);
```

---

## 🔄 Application Flow

A simplified application flow looks like this:

```text
User
  │
  ▼
CLI Menu
  │
  ▼
BankingService
  │
  ├───────────────┐
  ▼               ▼
Account Model   Repository
                  │
                  ▼
               Database
                  │
                  ▼
                SQLite
```

Example deposit flow:

```text
User chooses Deposit
        ↓
Select account
        ↓
Enter amount
        ↓
BankingService.deposit()
        ↓
Account.deposit()
        ↓
AccountRepository.update_balance()
        ↓
TransactionRepository.log()
        ↓
SQLite database updated
```

---

## 💻 CLI Menu

When the application starts, the following menu is displayed:

```text
===== PYTHON BANKING SYSTEM =====

1. Check Balance
2. Deposit
3. Withdraw
4. Transfer
5. Transaction History
0. Exit
```

---

## 👤 Default Demo Customer

The current learning implementation uses:

```text
Customer:
Jon
```

The application uses a get-or-create mechanism so the same customer is not duplicated every time the program starts.

---

## 💳 Default Accounts

Two demonstration accounts are created the first time the application runs.

### Savings Account

```text
Account Number:
ACC1001

Account Type:
Savings

Initial Balance:
1000
```

---

### Current Account

```text
Account Number:
ACC2001

Account Type:
Current

Initial Balance:
1000

Overdraft Limit:
500
```

After the accounts exist in SQLite, subsequent application runs load the stored balances instead of recreating the accounts.

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/Nandapratama716/python-sqlite-oop-banking-system.git
```

---

### 2. Enter the Project Directory

```bash
cd python-sqlite-oop-banking-system
```

---

### 3. Check Python

```bash
python --version
```

On some Windows installations:

```bash
py --version
```

---

### 4. Run the Application

```bash
python main.py
```

or:

```bash
py main.py
```

The SQLite database will be initialized automatically when the application runs.

---

## 🧪 Example Usage

### Check Balance

```text
===== PYTHON BANKING SYSTEM =====

1. Check Balance
2. Deposit
3. Withdraw
4. Transfer
5. Transaction History
0. Exit

Choose option: 1

Account number: ACC1001

Balance: 1000.0
```

---

### Deposit

```text
Choose option: 2

Account number: ACC1001
Deposit amount: 500

Deposit successful.
New balance: 1500.0
```

---

### Withdraw

```text
Choose option: 3

Account number: ACC1001
Withdraw amount: 200

Withdraw successful.
New balance: 1300.0
```

---

### Transfer

```text
Choose option: 4

From account: ACC1001
To account: ACC2001
Transfer amount: 300

Transfer successful.
Sender balance: 1000.0
Receiver balance: 1300.0
```

The exact balances depend on previous transactions stored in the database.

---

### Transaction History

```text
Choose option: 5

Account number: ACC1001

===== TRANSACTION HISTORY =====

DEPOSIT | 500.0 | 2026-09-16T19:31:07
WITHDRAW | 200.0 | 2026-09-16T19:31:10
TRANSFER_OUT | 300.0 | 2026-09-16T19:31:15
```

---

## ✅ Validation

The application currently handles several invalid operations.

### Invalid Deposit

Deposit amounts must be greater than zero.

```text
Error: Invalid deposit amount
```

---

### Insufficient Savings Balance

A Savings Account cannot withdraw beyond its current balance.

```text
Error: Insufficient funds
```

---

### Current Account Overdraft

A Current Account cannot withdraw beyond:

```text
balance + overdraft limit
```

Example:

```text
Balance: 1000
Overdraft: 500

Maximum available:
1500
```

Attempting to withdraw more produces:

```text
Error: Overdraft limit exceeded
```

---

### Invalid Account

If an account number does not exist:

```text
Account not found.
```

---

### Same-Account Transfer

The application prevents:

```text
ACC1001
↓
ACC1001
```

and displays:

```text
Cannot transfer to the same account.
```

---

## 🧠 OOP Concepts Used

This project applies several Object-Oriented Programming concepts.

### Classes and Objects

Examples:

```text
Customer
Account
SavingsAccount
CurrentAccount
```

---

### Inheritance

Both:

```text
SavingsAccount
CurrentAccount
```

inherit from:

```text
Account
```

---

### Method Overriding

Each account type can implement its own withdrawal rules.

For example:

```text
Savings Account
→ cannot exceed balance

Current Account
→ can use overdraft
```

---

### Encapsulation of Responsibilities

Different responsibilities are separated into:

```text
Models
Repositories
Services
Database
Presentation
```

---

## 💾 Persistence

One of the main goals of this project is understanding data persistence.

Without persistence:

```text
Program closes
↓
Data disappears
```

With SQLite:

```text
Program closes
↓
Data remains inside bank.db
↓
Program starts again
↓
Previous balances are loaded
```

This allows the banking system to maintain its state between application runs.

---

## 🔐 Security Notes

This project demonstrates basic backend architecture but should not be treated as a real banking application.

For a production financial system, additional features would be required, such as:

```text
Authentication
Authorization
Password hashing
Encryption
Database transactions
Audit logging
Concurrency handling
Secure API access
Fraud prevention
Financial precision handling
Automated testing
```

---

## 📚 What I Learned

Through this project, I practiced and strengthened my understanding of:

```text
Python fundamentals
Variables and data types
Functions
Loops
Exception handling
Object-Oriented Programming
Classes and objects
Inheritance
Method overriding
SQLite
SQL queries
Database persistence
Repository pattern
Service layer architecture
Separation of concerns
CLI development
Input validation
Transaction logging
Git and GitHub documentation
```

---

## 🚧 Possible Future Improvements

The project can be extended with:

- Interactive customer registration
- Dynamic account creation
- Multiple customers
- Account login/authentication
- PIN/password protection
- Improved transaction validation
- Database transaction rollback
- Automated unit tests
- REST API using FastAPI
- Web-based dashboard
- PostgreSQL migration
- SQLAlchemy ORM
- User authentication and authorization
- Better transaction reporting
- Docker support
- API documentation
- Sensitive data encryption

---

## 🗺️ Possible Development Roadmap

```text
Current CLI Application
        ↓
Improve Automated Tests
        ↓
FastAPI REST API
        ↓
Authentication
        ↓
SQLAlchemy
        ↓
PostgreSQL
        ↓
Web Frontend
        ↓
Docker Deployment
```

---

## 📖 Learning Context

This project was developed as part of my learning process in a **Python Full Stack AI Engineer course**.

The original starter project introduced:

```text
Python
SQLite
Object-Oriented Programming
Repository Layer
Service Layer
Banking Domain Models
```

During development, I expanded and tested the project by working on:

```text
Automatic database initialization
Customer persistence
Account persistence
Existing-account retrieval
Savings account validation
Current account overdraft behavior
Fund transfers
Transaction history retrieval
Persistent balances
Interactive CLI
Code organization
GitHub documentation
```

---

## 🙏 Credits

Starter project and learning material:

**Creative Online School**

Website:

```text
https://creativeonlineschool.com
```

The original source files include attribution to Creative Online School and identify the starter code as licensed under **Apache 2.0**.

This repository documents my learning implementation, testing process, modifications, and development progress based on that starter project.

---

## 📌 Project Status

```text
Core Python/OOP        ✅
SQLite Integration     ✅
Database Persistence   ✅
Savings Account        ✅
Current Account        ✅
Deposit                ✅
Withdraw               ✅
Overdraft Validation   ✅
Fund Transfer          ✅
Transaction History    ✅
Interactive CLI        ✅
Code Refactoring       ✅
Documentation          ✅
```

**Status: Completed — Learning Project v1**

---

## 👨‍💻 Author

**Nanda Pratama**

GitHub: [@Nandapratama716](https://github.com/Nandapratama716)

---

## ⭐ About This Repository

This repository is part of my personal learning documentation.

Instead of only storing the original course source code, I use this repository to document how I:

```text
understand the project
↓
run the original implementation
↓
identify problems
↓
debug the application
↓
improve persistence
↓
test banking operations
↓
refactor the code
↓
document the final result
```

The goal is to build a stronger understanding of backend development fundamentals before progressing into more advanced Full Stack AI engineering topics.