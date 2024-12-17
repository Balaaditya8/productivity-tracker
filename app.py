from flask import Flask, render_template
from datetime import datetime
from collections import defaultdict
import sqlite3
import math
app = Flask(__name__)

# Function to parse time strings
def parse_time(time_str):
    return datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")

# Function to calculate hourly usage data
def calculate_hourly_data():
    # Connect to the SQLite database to fetch app usage data
    conn = sqlite3.connect('app_usage.db')
    cursor = conn.cursor()
    
    # Query to fetch the app usage data from the database
    cursor.execute("SELECT app_name, start_time, end_time FROM app_usage ORDER BY start_time")
    app_usage = cursor.fetchall()
    
    # Close the database connection
    conn.close()
    
    # Dictionary to hold hourly data (key: hour, value: list of (app_name, time_spent))
    hourly_data = defaultdict(lambda: defaultdict(float))
    
    # Iterate through the fetched app usage data
    for usage in app_usage:
        app_name = usage[0]
        start_time = parse_time(usage[1])
        end_time = parse_time(usage[2])
        
        # Calculate time spent in minutes
        time_spent = math.ceil((end_time - start_time).seconds / 60)
        
        # Get the hour of the start time
        hour = start_time.hour
        
        # Accumulate time spent on the app in the respective hour
        hourly_data[hour][app_name] += time_spent
    
    # Ensure all 24 hours are represented, even if no data exists
    for hour in range(24):
        if hour not in hourly_data:
            hourly_data[hour] = {}
    
    return hourly_data

@app.route('/')
def index():
    # Get the hourly data
    hourly_data = calculate_hourly_data()
    
    # Pass the data to the HTML template
    return render_template('index.html', hourly_data=hourly_data)

if __name__ == '__main__':
    app.run(debug=True)
