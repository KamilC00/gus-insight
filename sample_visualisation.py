import pandas as pd
import matplotlib
matplotlib.use('Agg') 
import matplotlib.pyplot as plt
import sqlite3
import io
import base64


def plot_unemployment_data():
  query = "SELECT * FROM gus_data WHERE variable_id IN (7, 8);"
  try:
    with sqlite3.connect("database.db") as con:
      df = pd.read_sql_query(query, con)
      filtered_df = df[(df["unit_name"] == "POLSKA") & (df["year"] >= 2015) & (df["year"] <= 2020)].copy()
      filtered_df.drop(columns=["id", "unit_id", "unit_name"], inplace=True)
      filtered_df.rename(columns={"variable_id": "sex"}, inplace=True)
      filtered_df["sex"] = filtered_df["sex"].replace({7: "Mężczyźni", 8: "Kobiety"})

      pivot = filtered_df.pivot(index="year", columns="sex", values="value")
      pivot.plot(kind="bar")

      plt.title("Liczba osób bezrobotnych wg płci w Polsce (2015–2020)")
      plt.xlabel("Rok")
      plt.ylabel("Wartość")
      plt.xticks(rotation=0)
      plt.legend(title="Płeć")
      plt.tight_layout()
      
      buf = io.BytesIO()
      plt.savefig(buf, format="png")
      buf.seek(0)
      image_base64 = base64.b64encode(buf.read()).decode("utf-8")
      plt.close()

      return image_base64
  except Exception as e:
    print(f"An error occurred while fetching data: {e}")

def plot_inflation_data():
  query = "SELECT * FROM gus_data WHERE variable_id = 217230;"
  try:
    with sqlite3.connect("database.db") as con:
      df = pd.read_sql_query(query, con)
      filtered_df = df[(df["unit_name"] == "POLSKA") & (df["year"] >= 2015) & (df["year"] <= 2024)].copy()
      filtered_df.drop(columns=["id", "unit_id", "unit_name", "variable_id"], inplace=True)
      filtered_df.set_index("year")["value"].plot(kind="line")

      plt.title("Inflacja w Polsce w latach 2015-2024")
      plt.xlabel("Rok")
      plt.ylabel("Wartość")
      plt.xticks(rotation=0)
      plt.tight_layout()

      buf = io.BytesIO()
      plt.savefig(buf, format="png")
      buf.seek(0)
      image_base64 = base64.b64encode(buf.read()).decode("utf-8")
      plt.close()

      return image_base64
  except Exception as e:
    print(f"An error occurred while fetching data: {e}")

def plot_alcohol_data():
  query = "SELECT * FROM gus_data WHERE variable_id IN (8265, 5003);"
  try:
    with sqlite3.connect("database.db") as con:
      df = pd.read_sql_query(query, con)
      filtered_df = df[(df["unit_name"] == "POLSKA") & (df["year"] >= 2015) & (df["year"] <= 2024)].copy()
      filtered_df.drop(columns=["id", "unit_id", "unit_name"], inplace=True)
      filtered_df.rename(columns={"variable_id": "typ"}, inplace=True)
      filtered_df["typ"] = filtered_df["typ"].replace({8265: "wódka czysta 40%", 5003: "piwo jasne pełne"})
      pivot = filtered_df.pivot(index="year", columns="typ", values="value")
      pivot.plot(kind="line")

      plt.title("Ceny alkoholu w Polsce w latach 2015-2024")
      plt.xlabel("Rok")
      plt.ylabel("Wartość")
      plt.xticks(rotation=0)
      plt.legend(title="Typ")
      plt.tight_layout()

      buf = io.BytesIO()
      plt.savefig(buf, format="png")
      buf.seek(0)
      image_base64 = base64.b64encode(buf.read()).decode("utf-8")
      plt.close()

      return image_base64
  except Exception as e:
    print(f"An error occurred while fetching data: {e}")


def plot_fuel_data():
  query = "SELECT * FROM gus_data WHERE variable_id = 196398;"
  try:
    with sqlite3.connect("database.db") as con:
      df = pd.read_sql_query(query, con)
      filtered_df = df[(df["unit_name"] == "POLSKA") & (df["year"] >= 2015) & (df["year"] <= 2024)].copy()
      filtered_df.drop(columns=["id", "unit_id", "unit_name", "variable_id"], inplace=True)
      filtered_df.set_index("year")["value"].plot(kind="line")

      plt.title("Ceny paliw w Polsce w latach 2015-2024")
      plt.xlabel("Rok")
      plt.ylabel("Wartość")
      plt.xticks(rotation=0)
      plt.tight_layout()

      buf = io.BytesIO()
      plt.savefig(buf, format="png")
      buf.seek(0)
      image_base64 = base64.b64encode(buf.read()).decode("utf-8")
      plt.close()

      return image_base64
  except Exception as e:
    print(f"An error occurred while fetching data: {e}")
    
if __name__ == "__main__":
  plot_unemployment_data()
  plot_inflation_data()
  plot_alcohol_data()