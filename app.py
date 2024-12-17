from flask import Flask, render_template, request
from datetime import datetime
from collections import defaultdict
import sqlite3
import math
app = Flask(__name__)

# Function to parse time strings
def parse_time(time_str):
    return datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")

# Function to calculate hourly usage data
def calculate_hourly_data(target_date=None):
    conn = sqlite3.connect('app_usage.db')
    cursor = conn.cursor()
    
    # Query to fetch app usage data (filter by date if provided)
    if target_date:
        cursor.execute("""
            SELECT app_name, start_time, end_time 
            FROM app_usage 
            WHERE DATE(start_time) = ?
            ORDER BY start_time
        """, (target_date,))
    else:
        cursor.execute("SELECT app_name, start_time, end_time FROM app_usage ORDER BY start_time")
    
    app_usage = cursor.fetchall()
    conn.close()
    
    hourly_data = defaultdict(lambda: defaultdict(float))
    
    # Process fetched data
    for usage in app_usage:
        app_name = usage[0]
        start_time = parse_time(usage[1])
        end_time = parse_time(usage[2])
        
        time_spent = math.ceil((end_time - start_time).seconds / 60)
        hour = start_time.hour
        hourly_data[hour][app_name] += time_spent

    # Fill all 24 hours to ensure proper rendering
    for hour in range(24):
        if hour not in hourly_data:
            hourly_data[hour] = {}
    
    return hourly_data


@app.route('/', methods=['GET'])
def index():
    target_date = request.args.get('date')  
    if not target_date:
        target_date = datetime.now().strftime('%Y-%m-%d')
    
    hourly_data = calculate_hourly_data(target_date)
    return render_template('index.html', hourly_data=hourly_data, target_date=target_date)

if __name__ == '__main__':
    app.run(debug=True)
