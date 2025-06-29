# This script connects to a SQLite database, runs a series of SQL queries to explore the Chinook database,
# and loads results into pandas DataFrames for basic analysis and display.

import sqlite3
import pandas as pd

def main(): 
    # Connect to the SQLite database
    conn = sqlite3.connect(r'C:\Documents\Chinook_Database\chinook.db')

    # 1. List all tables in the database
    print(" Tables in the database:")
    tables = pd.read_sql_query("SELECT name FROM sqlite_master WHERE type='table';", conn)
    print(tables)

    # 2. Preview first few rows of the 'albums' table
    print("\n Sample rows from 'albums':")
    print(pd.read_sql_query("SELECT * FROM albums LIMIT 10;", conn))

    # 3. Load full 'albums' table and count rows
    albums_table = pd.read_sql_query("SELECT * FROM albums;", conn)
    print("\n Full 'albums' table:")
    print(albums_table)
    print(f"\n🔢 There are {len(albums_table)} albums in the database.")

    # 4. View schema of 'albums' table
    print("\n Schema of 'albums':")
    album_schema = pd.read_sql_query("PRAGMA table_info(albums);", conn)
    print(album_schema)

    # 5. List all albums with their corresponding artist names
    print("\n Albums and their artists:")
    query = """
    SELECT albums.Title, artists.Name AS Artist
    FROM albums
    INNER JOIN artists ON albums.ArtistId = artists.ArtistId;
    """
    df = pd.read_sql_query(query, conn)
    print(df.head())

    # 6. View schema and column names of 'customers' table
    print("\n Schema of 'customers' table:")
    df = pd.read_sql_query("PRAGMA table_info(customers);", conn)
    print(df)
    print("Columns:", df['name'].tolist())

    customers_table = pd.read_sql_query("SELECT * FROM customers;", conn)
    print("Columns (via DataFrame):", customers_table.columns.tolist())

    # 7. Count customers per country, ordered from most to least
    print(f"\n There are {len(customers_table)} customers in the database.")
    query = """
    SELECT Country, COUNT(CustomerId) AS num_customers
    FROM customers
    GROUP BY Country
    ORDER BY num_customers DESC;
    """
    df = pd.read_sql_query(query, conn)
    print(df)

    # 8. Preview raw invoice and track data (optional)
    print("\n Sample 'invoice_items':")
    print(pd.read_sql_query("SELECT * FROM invoice_items LIMIT 5;", conn))

    print("\n Sample 'tracks':")
    print(pd.read_sql_query("SELECT * FROM tracks LIMIT 5;", conn))

    # 9. Top 5 most sold tracks by quantity
    print("Top 5 most sold tracks:")
    query = """
    SELECT tracks.Name AS track_name,
           SUM(invoice_items.Quantity) AS total_quantity
    FROM invoice_items
    INNER JOIN tracks ON tracks.TrackId = invoice_items.TrackId
    GROUP BY invoice_items.TrackId
    ORDER BY total_quantity DESC
    LIMIT 5;
    """
    df = pd.read_sql_query(query, conn)
    print(df)

    # Close the database connection
    conn.close()

main()
