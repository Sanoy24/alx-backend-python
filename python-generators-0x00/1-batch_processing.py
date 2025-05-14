# 1-batch_processing.py

import mysql.connector
import os
from dotenv import load_dotenv
from utils.db_utils import get_connection
import logging

# Set up logging for the application
logging.basicConfig(
    level=logging.INFO,  # Set log level (DEBUG, INFO, WARNING, ERROR)
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def connect_to_prodev():
    """Connects to the ALX_prodev database in MySQL."""
    try:
        connection = get_connection()
        if connection.is_connected():
            # print("Successfully connected to ALX_prodev database")
            return connection
    except mysql.connector.Error as e:
        print(f"Error connecting to MySQL database ALX_prodev: {e}")
        return None


def stream_users_in_batches(batch_size: int):
    """
    Fetches rows from the user_data table in batches using a generator.
    Uses no more than 1 loop.
    """
    connection = connect_to_prodev()
    if not connection:
        print("Failed to connect to database for streaming.")
        return

    cursor = connection.cursor(dictionary=True)  # Get rows as dictionaries
    offset = 0

    # Loop 1: Fetches data in batches
    while True:
        query = f"SELECT user_id, name, email, age FROM user_data ORDER BY user_id LIMIT %s OFFSET %s"
        try:
            cursor.execute(query, (batch_size, offset))
            batch = cursor.fetchall()
        except mysql.connector.Error as e:
            print(f"Error executing query: {e}")
            break  # Exit loop on query error

        if not batch:  # No more data to fetch
            break

        yield batch  # Yield the current batch

        offset += batch_size

    cursor.close()
    connection.close()


def batch_processing(batch_size: int):
    """
    Processes each batch from stream_users_in_batches to filter users over the age of 25.
    Uses no more than 2 additional loops (1 here, 1 in stream_users_in_batches,
    and 1 for filtering within this loop, totaling 3 loops for the script).
    """
    print(f"Processing users in batches of {batch_size}. Filtering for age > 25.")
    processed_users_count = 0

    # Loop 2: Iterates through batches yielded by stream_users_in_batches
    for batch in stream_users_in_batches(batch_size):
        filtered_batch_users = []
        # Loop 3: Iterates through users within a batch for filtering
        for user in batch:
            try:
                # Ensure age is treated as a number for comparison
                if float(user["age"]) > 25:
                    filtered_batch_users.append(user)
            except ValueError:
                print(
                    f"Warning: Could not convert age '{user['age']}' to float for user_id {user['user_id']}"
                )
                continue  # Skip this user if age is not a valid number

        if filtered_batch_users:
            print(
                f"--- Batch Processed: Found {len(filtered_batch_users)} users over 25 ---"
            )
            for user in filtered_batch_users:
                print(
                    f"  User ID: {user['user_id']}, Name: {user['name']}, Email: {user['email']}, Age: {user['age']}"
                )
                processed_users_count += 1
        else:
            print("--- Batch Processed: No users over 25 in this batch ---")

    print(
        f"\nBatch processing complete. Total users over 25 processed: {processed_users_count}"
    )


if __name__ == "__main__":
    print("Attempting to process users with current DB credentials...")
    # Set a batch size for processing
    users_batch_size = 10  # You can change this value
    batch_processing(users_batch_size)
