import sqlite3

con = None

def connect_db():
  global con

  try:
    con = sqlite3.connect('database.db')
  except sqlite3.Error as e:
    raise Exception(f"Error connecting to database: {e}")

def execute_query(query):
  global con

  try:
    if not con:
      connect_db()

    cursor = con.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    con.commit()
    cursor.close()

    return result
  except Exception as e:
    print(f"An error occurred: {e}")
