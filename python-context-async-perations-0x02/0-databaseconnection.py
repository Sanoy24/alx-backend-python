import sqlite3


class DatabaseConnection:
    def __init__(self, dbname):
        self.dbname = dbname
        self.connection = None

    def __enter__(self):
        self.connection = sqlite3.connect(self.dbname)
        return self.connection

    def __exit__(self, exc_type, exc_value, exc_trace):
        if self.connection():
            return self.connection.close()


with DatabaseConnection("users.db") as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    print(cursor.fetchall())
