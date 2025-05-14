import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()


def stream_user_ages():
    """Generator that yields user ages one by one from the user_data table."""
    try:
        conn = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database="ALX_prodev",
        )
        cursor = conn.cursor()
        cursor.execute("SELECT age FROM user_data")

        for (age,) in cursor:
            yield float(age)

    except mysql.connector.Error as err:
        print(f"Database error: {err}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def compute_average_age():
    """Compute the average age of users using a generator."""
    total_age = 0
    count = 0

    for age in stream_user_ages():
        total_age += age
        count += 1

    average_age = total_age / count if count else 0
    print(f"Average age of users: {average_age:.2f}")
