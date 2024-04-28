from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
import subprocess
import threading

app = Flask(__name__)
socketio = SocketIO(app)  # Define the socketio object

# Function to execute autotimer.py and emit its output over WebSocket
def track_terminal():
    process = subprocess.Popen(['python', '../AutoTimer-master/env/autotimer.py'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    for line in iter(process.stdout.readline, b''):
        socketio.emit('terminal_output', {'output': line.decode('utf-8')})
    process.stdout.close()
    process.wait()

# Route for serving the HTML page
@app.route('/')
def index():
    return render_template('index.html')

# Route for serving the track.html page and initiating terminal tracking
@app.route('/track')
def track():
    threading.Thread(target=track_terminal).start()  # Start tracking the terminal in a separate thread
    return render_template('track.html')

# WebSocket handler for receiving commands
@socketio.on('command')
def handle_command(data):
    # Handle commands received from the client, if needed
    pass

# WebSocket route for live tracking updates
@socketio.on('connect', namespace='/live_tracking')
def handle_live_tracking_connect():
    print('Client connected to live tracking')

# Handle live tracking messages
@socketio.on('live_tracking_message', namespace='/live_tracking')
def handle_live_tracking_message(message):
    # Process live tracking message received from client
    pass

if __name__ == "__main__":
    socketio.run(app, debug=True)
