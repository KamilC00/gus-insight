from db import execute_query

def create_tables():
  create_users_table = """
CREATE TABLE IF NOT EXISTS users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT NOT NULL,
  password_hash TEXT NOT NULL,
  salt TEXT NOT NULL
);
"""

  create_gus_data_table = """
CREATE TABLE IF NOT EXISTS gus_data (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  variable_id INTEGER NOT NULL,
  unit_id INTEGER NOT NULL,
  unit_name TEXT NOT NULL,
  year INTEGER NOT NULL,
  value REAL NOT NULL
);
"""

  execute_query(create_users_table)
  execute_query(create_gus_data_table)

if __name__ == "__main__":
  create_tables()
  print("Database initialized successfully.")