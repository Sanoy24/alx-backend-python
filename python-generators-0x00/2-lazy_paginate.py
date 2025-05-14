# 2-lazy_paginate.py

import mysql.connector
import os

from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")


def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME
        )
        if connection.is_connected():
            return connection
    except mysql.connector.Error as e:
        print(f"Error connecting to MySQL database ALX_prodev: {e}")
        return None


def paginate_users(page_size: int, offset: int, connection):
    """
    Fetches a specific page of users from the user_data table.
    Assumes 'connection' is an active database connection.
    Returns a list of user records for the page, or an empty list if no more data.
    """
    if not connection or not connection.is_connected():
        print("Database connection is not active for paginate_users.")
        return []

    cursor = None  # Initialize cursor to None
    try:
        cursor = connection.cursor(dictionary=True)  # Get rows as dictionaries
        query = "SELECT user_id, name, email, age FROM user_data ORDER BY user_id LIMIT %s OFFSET %s"
        cursor.execute(query, (page_size, offset))
        page_data = cursor.fetchall()
        return page_data
    except mysql.connector.Error as e:
        print(f"Error executing query in paginate_users: {e}")
        return []  # Return empty list on error to allow lazy_paginate to terminate
    finally:
        if cursor:
            cursor.close()


def lazy_paginate(page_size: int):
    """
    Lazily fetches paginated data from the user_data table.
    It yields one page of data at a time, fetching the next page only when needed.
    Uses only one primary loop for iterating through pages.
    """
    connection = get_db_connection()
    if not connection:
        print("Failed to connect to database for lazy pagination.")
        return  # Stop generation if no DB connection

    current_offset = 0

    # The single loop for fetching pages
    while True:
        # print(f"lazy_paginate: Requesting page with offset {current_offset}, page_size {page_size}")
        page = paginate_users(
            page_size=page_size, offset=current_offset, connection=connection
        )

        if not page:  # If paginate_users returns an empty list (no more data or error)
            break  # Exit the loop

        yield page  # Yield the current page

        current_offset += page_size  # Prepare offset for the next page

    if connection and connection.is_connected():
        connection.close()
