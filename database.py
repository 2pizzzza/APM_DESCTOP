import sqlite3

from faker import Faker


class Database:
    def __init__(self, db_name="enterprise.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        with self.conn:
            self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS employees (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                position TEXT NOT NULL
            )
        ''')

            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS finances (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    budget REAL NOT NULL,
                    income REAL NOT NULL,
                    expense REAL NOT NULL
                )
            ''')

    def execute_query(self, query, params=None):
        if params:
            self.cursor.execute(query, params)
        else:
            self.cursor.execute(query)
        self.conn.commit()

    def populate_fake_data(self, num_entries=10):
        fake = Faker()
        for _ in range(num_entries):
            name = fake.name()
            position = fake.job()
            self.cursor.execute("INSERT INTO employees (name, position) VALUES (?, ?)", (name, position))

        for _ in range(num_entries):
            budget = fake.random_int(1000, 10000)
            income = fake.random_int(500, 5000)
            expense = fake.random_int(100, 2000)
            self.cursor.execute("INSERT INTO finances (budget, income, expense) VALUES (?, ?, ?)",
                                (budget, income, expense))

        self.conn.commit()

    def fetch_all(self, query, params=None):
        if params:
            self.cursor.execute(query, params)
        else:
            self.cursor.execute(query)
        return self.cursor.fetchall()

    def close_connection(self):
        self.conn.close()
