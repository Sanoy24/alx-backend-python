import sqlite3


class ExecuteQuery:
    def __init__(self, query, params=None, dbname="users.db"):
        self.query = query
        self.params = params
        self.dbname = dbname
        self.conn = None
        self.cursor = None
        self.result = None

    def __enter__(self):
        self.conn = sqlite3.connect(self.dbname)
        self.cursor = self.conn.cursor()
        self.cursor.execute(self.query, self.params)
        self.result = self.cursor.fetchall()
        return self.result

    def __exit__(self, exc_type, exc_val, exc_trace):
        if exc_type:
            self.conn.rollback()
            print(f"[ERROR] Rolled back due to {exc_val}")
        else:
            self.conn.commit()
            self.cursor.close()
            self.conn.close()


query = "SELECT * FROM users WHERE age > ?"
params = (25,)

with ExecuteQuery(query=query, params=params) as users:
    for user in users:
        print(user)
