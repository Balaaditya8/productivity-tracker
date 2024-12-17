import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('app_usage.db')
cursor = conn.cursor()

# Query all rows from the app_usage table
cursor.execute('SELECT * FROM app_usage')

# Fetch all results
rows = cursor.fetchall()

# Print each row
for row in rows:
    print(row)

# Close the connection
conn.close()