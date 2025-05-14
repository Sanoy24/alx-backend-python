import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()


def get_connection():
    """Returns a connection to the specified MySQL database."""
    try:
        conn = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME"),
        )
        return conn
    except mysql.connector.Error as err:
        print(f"Connection error: {err}")
        return None
