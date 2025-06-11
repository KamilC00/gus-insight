from db import execute_query
from fetch_data import fetch_data
import os

def check_db():
  
  check_users_table = """
SELECT name FROM sqlite_master 
WHERE type='table' AND name='users';
"""
  check_gus_data_table = """
SELECT name FROM sqlite_master 
WHERE type='table' AND name='gus_data';
"""

  if not os.path.exists("database.db"):
    return False
  
  try:
      users_result = execute_query(check_users_table)
      gus_data_result = execute_query(check_gus_data_table)
      
      users_exists = len(users_result) > 0 if users_result else False
      gus_data_exists = len(gus_data_result) > 0 if gus_data_result else False
      
      return users_exists and gus_data_exists
  except Exception as e:
      print(f"Error checking tables: {e}")
      return False


def create_tables():
  create_users_table = """
CREATE TABLE IF NOT EXISTS users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT NOT NULL,
  password_hash TEXT NOT NULL
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

def create_admin_user():
  
  insert_users_table = """
INSERT INTO users (username, password_hash) VALUES (
  'admin',
  '$pbkdf2-sha256$29000$tbbWmhNCyDmntHZuLaX0Hg$g3MCahD/4QRsqVGNOQKea454GTpPbkCcXAUVDff1COo'
);
"""
  execute_query(insert_users_table)

def init_db():
  if not check_db():
    create_tables()
    print("Tables created successfully.")
    create_admin_user()
    print("Admin user created successfully.")
    print("Database initialized successfully.")
    fetch_data()
  else:
    print("Databese already initialized")