from flask import Flask, send_file
import json
import matplotlib.pyplot as plt
from io import BytesIO

app = Flask(__name__)

@app.route('/')
def index():
    # Read JSON data from file
    with open('activities.json', 'r') as file:
        data = json.load(file)

    # Calculate total time for each activity
    activity_times = {}
    for activity in data["activities"]:
        total_seconds = sum(entry["days"] * 24 * 3600 + entry["hours"] * 3600 + entry["minutes"] * 60 + entry["seconds"] for entry in activity["time_entries"])
        activity_times[activity["name"]] = total_seconds

    # Sort activities by total time
    sorted_activities = sorted(activity_times.items(), key=lambda x: x[1], reverse=True)

    # Extract activity names and times
    activity_names = [entry[0] for entry in sorted_activities]
    activity_seconds = [entry[1] for entry in sorted_activities]

    # Convert seconds to hours for better readability
    activity_hours = [seconds / 3600 for seconds in activity_seconds]

    # Plot the bar chart with improved styling
    plt.figure(figsize=(12, 8))
    plt.barh(activity_names, activity_hours, color='skyblue', edgecolor='black')  # Add black edges to bars
    plt.xlabel('Time Spent (hours)', fontsize=14)
    plt.ylabel('Activity', fontsize=14)
    plt.title('Time Spent on Different Activities', fontsize=16, fontweight='bold')  # Increase title font size and add bold
    plt.grid(axis='x', linestyle='--', alpha=0.7)
    plt.xticks(fontsize=12)  # Increase tick label font size
    plt.yticks(fontsize=12)  # Increase tick label font size
    plt.gca().invert_yaxis()  # Invert y-axis to have the highest activity on top
    plt.tight_layout()

    # Save plot to a BytesIO object
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)

    # Return the image file
    return send_file(buffer, mimetype='image/png')

@app.route('/real-time-graph')
def real_time_graph():
    # Call the index function to generate the real-time graph and return it
    return index()

if __name__ == '__main__':
    app.run(debug=True)
