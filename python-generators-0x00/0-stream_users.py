import mysql.connector
import os
from dotenv import load_dotenv
from itertools import islice
from utils.db_utils import get_connection

load_dotenv()


def stream_users():
    """Generator that yields users one by one from the user_data table"""
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM user_data")
        for row in cursor:
            yield row

    except mysql.connector.Error as err:
        print(f"Database error: {err}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


# for user in islice(stream_users(), 6):
#     print(user)
