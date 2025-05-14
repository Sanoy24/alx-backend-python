import mysql.connector
import os
from dotenv import load_dotenv
from itertools import islice

load_dotenv()


def stream_users():
    """Generator that yields users one by one from the user_data table"""
    try:
        conn = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database="ALX_prodev",
        )
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
