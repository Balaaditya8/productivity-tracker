# App Usage Tracker
*Only for Mac*
A simple Flask-based application that tracks app usage and displays time spent on each app for every hour of the day. The app retrieves app usage data from a SQLite database, processes it, and presents it in a clean, user-friendly web interface.

---

## Features

- Displays app usage for each hour of the day in a structured format.
- Provides a scrollable view for each hour, showing apps used during that hour with time spent.
- Organized and responsive UI with separate boxes for each hour and app.

---

## Technologies Used

- **Python**: Backend logic using Flask.
- **Flask**: Web framework for routing and rendering.
- **SQLite**: Database for storing app usage data.
- **HTML/CSS**: Frontend design and layout.
- **JavaScript**: Enables smooth scrolling behavior.

---
## Running the App

### Step 1: Update the Database
Before running the app, populate or update the database with usage data using tracker.py:

```bash
python tracker.py
```
### Step 2: Start the Flask App
Run the Flask server:
```bash
python app.py
```
---
