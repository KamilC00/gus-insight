import requests
from db import execute_query

GUS_BASE_URL = "https://bdl.stat.gov.pl"
API_PATHS = [
  "/api/v1/data/by-variable/6",
  "/api/v1/data/by-variable/7",
  "/api/v1/data/by-variable/8"
]

def save_to_db(data):
  rows_joined = ",".join([str(row) for row in data])
  insert_query = f"INSERT INTO gus_data (variable_id, unit_id, unit_name, year, value) VALUES {rows_joined};"
  truncate_query = "DELETE FROM gus_data;"
  try:
    execute_query(truncate_query)
    execute_query(insert_query)
    print("Data fetched and inserted successfully.")
  except Exception as e:
    print(f"An error occurred while inserting data: {e}")

def fetch_data():
  rows = []

  for path in API_PATHS:
    url = f"{GUS_BASE_URL}{path}"
    response = requests.get(url)
    if response.status_code == 200:
      data = response.json()

      variable_id = data.get("variableId")
      results = data.get("results", [])

      for result in results:
        unit_id = result.get("id")
        unit_name = result.get("name")
        values = result.get("values", [])

        for value in values:
          year = value.get("year")
          value = value.get("val")

          rows.append((variable_id, unit_id, unit_name, year, value))
    else:
      print(f"Failed to fetch data from {url}: {response.status_code}")
    
  save_to_db(rows)

if __name__ == "__main__":
  fetch_data()