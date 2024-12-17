import sqlite3

# Connect to SQLite database (creates the file if it doesn't exist)
conn = sqlite3.connect('app_usage.db')
cursor = conn.cursor()

# Create a table to store the data if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS app_usage (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT,
        active_app TEXT,
        duration INTEGER
    )
''')

conn.commit()
conn.close()