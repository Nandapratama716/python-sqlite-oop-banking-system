"""
Project: SQLite + Python OOP Based Banking System 

Author  : Creative Online School
License : Apache 2.0
URL     : https://creativeonlineschool.com
"""

import sqlite3

class Database:
    def __init__(self, db_name="bank.db"):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()

    def execute(self, query, params=()):
        self.cursor.execute(query, params)
        self.connection.commit()
        return self.cursor.lastrowid

    def fetchone(self, query, params=()):
        self.cursor.execute(query, params)
        return self.cursor.fetchone()

    def fetchall(self, query, params=()):
        self.cursor.execute(query, params)
        return self.cursor.fetchall()

    def initialize(self, schema_file="schema.sql"):
        with open(schema_file, "r") as file:
            schema = file.read()

        self.connection.executescript(schema)
        self.connection.commit()
