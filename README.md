# alx-backend-python

# Python Generators - ALX Backend Task

## Overview

This project demonstrates how to use Python generators with a MySQL database to handle large datasets efficiently. Generators are ideal for streaming data, batch processing, paginated fetching, and memory-efficient aggregation. Each task builds on the previous to demonstrate progressive use of generators in real-world backend scenarios.

---

## 🧠 Task 0: Getting Started with Python Generators

### Objective:

Create a Python script that sets up a MySQL database and table, and populates it with user data from a CSV file.

### Instructions:

- Create a MySQL database: `ALX_prodev`
- Create a table: `user_data` with the following fields:
  - `user_id` (UUID, Primary Key, Indexed)
  - `name` (VARCHAR, NOT NULL)
  - `email` (VARCHAR, NOT NULL)
  - `age` (DECIMAL, NOT NULL)
- Populate the table using data from `user_data.csv`

### Function Prototypes:

```python
def connect_db()
def create_database(connection)
def connect_to_prodev()
def create_table(connection)
def insert_data(connection, data)
```

### File:

- `seed.py`

---

## 🔁 Task 1: Generator That Streams Rows from SQL Database

### Objective:

Create a generator that fetches rows one by one from the database.

### Instructions:

- Implement the function:

```python
def stream_users()
```

- Use the `yield` keyword to stream data from `user_data` one row at a time.

### Constraints:

- Only one loop is allowed.

### File:

- `0-stream_users.py`

---

## 📦 Task 2: Batch Processing Large Data

### Objective:

Create a generator to fetch and process users in batches.

### Instructions:

- Implement two functions:

```python
def stream_users_in_batches(batch_size)
def batch_processing(batch_size)
```

- `stream_users_in_batches`: yields data in chunks of `batch_size`
- `batch_processing`: filters and processes users over the age of 25

### Constraints:

- Use at most 3 loops
- Use the `yield` keyword for batch streaming

### File:

- `1-batch_processing.py`

---

## 📃 Task 3: Lazy Loading Paginated Data

### Objective:

Simulate pagination using a generator to lazily fetch each page of data.

### Instructions:

- Implement a generator:

```python
def lazy_paginate(page_size)
```

- Internally use a helper:

```python
def paginate_users(page_size, offset)
```

### Constraints:

- Only one loop allowed
- Use `yield` to load pages lazily

### File:

- `2-lazy_paginate.py`

---

## 📊 Task 4: Memory-Efficient Aggregation with Generators

### Objective:

Use a generator to calculate the average age of users without loading all data into memory.

### Instructions:

- Implement:

```python
def stream_user_ages()
```

- Use it to compute:

```python
def compute_average_age()
```

### Constraints:

- No use of SQL `AVERAGE`
- At most 2 loops
- Must use a generator

### Output:

```
Average age of users: <calculated_average>
```

### File:

- `4-stream_ages.py`

---

## 🗂️ Repository Structure

```
alx-backend-python/
└── python-generators-0x00/
    ├── seed.py
    ├── 0-stream_users.py
    ├── 1-batch_processing.py
    ├── 2-lazy_paginate.py
    ├── 4-stream_ages.py
    ├── user_data.csv
    └── README.md
```

---

## 💡 Notes

- All scripts must handle database connections cleanly.
- Focus on generator logic for memory efficiency.
- Avoid unnecessary data loading or storage.
