import sqlite3


class Database:
    def __init__(self, db_name="enterprise.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_table()  # Вызов метода create_table при создании объекта

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

    def fetch_all(self, query, params=None):
        if params:
            self.cursor.execute(query, params)
        else:
            self.cursor.execute(query)
        return self.cursor.fetchall()

    def close_connection(self):
        self.conn.close()
