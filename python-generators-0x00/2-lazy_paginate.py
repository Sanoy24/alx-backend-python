import mysql.connector
import os
from dotenv import load_dotenv
from utils.db_utils import get_connection


def paginate_users(page_size, offset):
    """Fetch a single page of users from the database based on page size and offset."""
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM user_data LIMIT %s OFFSET %s"
        cursor.execute(query, (page_size, offset))
        results = cursor.fetchall()
        return results

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return []
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def lazy_paginate(page_size):
    """Generator that yields pages of users lazily using paginate_users."""
    offset = 0
    while True:
        page = paginate_users(page_size, offset)
        if not page:
            break
        yield page
        offset += page_size
