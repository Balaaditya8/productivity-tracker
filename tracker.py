import subprocess
import time
import sqlite3
from datetime import datetime

# Function to get the active app using AppleScript
def get_active_app():
    script = '''
    tell application "System Events"
        set frontApp to name of first application process whose frontmost is true
    end tell
    return frontApp
    '''
    active_app = subprocess.run(['osascript', '-e', script], stdout=subprocess.PIPE).stdout.decode('utf-8').strip()
    return active_app

# Connect to SQLite database (creates the file if it doesn't exist)
conn = sqlite3.connect('app_usage.db')
cursor = conn.cursor()

# Create a table to store the data if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS app_usage (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        app_name TEXT,
        start_time TEXT,
        end_time TEXT,
        duration INTEGER
    )
''')

# Dictionary to store app usage with start and end times
prev_app = None
prev_time = None

while True:
    active_app = get_active_app()
    current_time = datetime.now()

    if active_app != prev_app:
        if prev_app is not None:
            # Calculate the duration in seconds
            duration = (current_time - prev_time).total_seconds()

            # Insert the data into SQLite
            cursor.execute('''
                INSERT INTO app_usage (app_name, start_time, end_time, duration)
                VALUES (?, ?, ?, ?)
            ''', (prev_app, prev_time.strftime('%Y-%m-%d %H:%M:%S'), current_time.strftime('%Y-%m-%d %H:%M:%S'), duration))
            conn.commit()

            # Print to the console for debugging
            print(f"App: {prev_app} | Start Time: {prev_time} | End Time: {current_time} | Duration: {duration} seconds")
        
        # Update the current app and start time
        prev_app = active_app
        prev_time = current_time

    time.sleep(5)  # Check every 5 seconds
