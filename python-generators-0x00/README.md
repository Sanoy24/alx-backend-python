# Python Generators - Task 0: Getting Started with Python Generators

# Task - 0

## Objective

This task demonstrates how to use Python to interact with a MySQL database and stream data efficiently using **generators**. The main goal is to populate a MySQL database with user data from a CSV file and prepare for streaming rows one by one in subsequent tasks.

## Project Structure

```
python-generators-0x00/
├── seed.py          # Script to create database, table, and insert CSV data
├── user_data.csv    # Sample user data to seed the database
└── README.md        # Project documentation
```

## Requirements

- Python 3.6+
- MySQL server
- Required Python packages:
  - `mysql-connector-python`
  - `python-dotenv`

Install dependencies using:

```bash
pip install -r requirements.txt
```

## Environment Variables

Create a `.env` file in the root of your project to store your MySQL credentials:

```
DB_HOST=your_host
DB_USER=your_user
DB_PASSWORD=your_password
DB_NAME=ALX_prodev
```

## Function Prototypes

The following functions are implemented in `seed.py`:

- `connect_db()` – Connects to the MySQL server
- `create_database(connection)` – Creates the `ALX_prodev` database if it does not exist
- `connect_to_prodev()` – Connects to the `ALX_prodev` database
- `create_table(connection)` – Creates the `user_data` table with UUID primary key and required fields
- `insert_data(connection, data)` – Inserts data from the CSV into the `user_data` table

## Usage

To run the script and set up the database:

```bash
python python-generators-0x00/seed.py
```

This will:

1. Connect to MySQL
2. Create the `ALX_prodev` database (if not already created)
3. Create the `user_data` table (if not already created)
4. Insert data from `user_data.csv` into the table

# Task 1: Generator that Streams Rows from SQL Database

## Objective

Create a Python generator function that streams rows one by one from a MySQL database table called `user_data`.

## Description

The function `stream_users()` connects to the MySQL database `ALX_prodev` and yields each row from the `user_data` table one at a time. This is a memory-efficient approach to process large datasets, as it avoids loading the entire result set into memory.

## Requirements

- Use the `yield` keyword to implement a Python generator.
- Fetch rows one by one from the `user_data` table.
- The function should use no more than **one loop**.
- The function must be implemented in `0-stream_users.py`.

## Function Prototype

```python
def stream_users()
```

## Usage Example

```python
from 0-stream_users import stream_users

for user in stream_users():
    print(user)
```

## File

- `0-stream_users.py`
