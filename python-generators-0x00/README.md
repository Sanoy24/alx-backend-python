# Python Generators - Task 0: Getting Started with Python Generators

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
