import mysql.connector
from dotenv import load_dotenv
import os
from mysql.connector import errorcode
import csv
import uuid

# DB_HOST=localhost
# DB_USER=root
# DB_PASSWORD=sanoy
# DB_NAME=ALX_prodev

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")


def connect_db():
    try:
        conn = mysql.connector.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD)
        print("Connected to mysql server")
        return conn

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None


def create_database(connection):
    cursor = connection.cursor()
    try:
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
        print(f"Database '{DB_NAME}' ensured.")
    except mysql.connector.Error as err:
        print(f"Failed creating database: {err}")
    cursor.close()


def connect_to_prodev():
    try:
        conn = mysql.connector.connect(
            host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME
        )
        print(f"Connected to database '{DB_NAME}'.")
        return conn
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None


def create_table(connection):
    cursor = connection.cursor()
    table_query = """
    CREATE TABLE IF NOT EXISTS user_data (
        user_id CHAR(36) PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL,
        age DECIMAL NOT NULL,
        INDEX(user_id)
    )
    """
    cursor.execute(table_query)
    print("Table 'user_data' ensured.")
    cursor.close()


def insert_data(connection, data):
    cursor = connection.cursor()
    for row in data:
        try:
            user_id = str(uuid.uuid4())
            cursor.execute(
                """
                INSERT INTO user_data (user_id, name, email, age)
                VALUES (%s, %s, %s, %s)
            """,
                (user_id, row["name"], row["email"], row["age"]),
            )
        except mysql.connector.Error as err:
            print(f"Insert error: {err}")
    connection.commit()
    print("Data inserted.")
    cursor.close()


def load_csv_data(file_path):
    with open(file_path, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)


if __name__ == "__main__":
    connection = connect_db()
    if connection:
        create_database(connection)
        connection.close()

    db_conn = connect_to_prodev()
    if db_conn:
        create_table(db_conn)
        csv_data = load_csv_data("python-generators-0x00/user_data.csv")
        insert_data(db_conn, csv_data)
        db_conn.close()
