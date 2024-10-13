# MiC3 Data Engineering Assessment - Problem Set 1 Task A
# 12 October 2024
# Author: Shashi Hagroo

from flask import Flask, request, jsonify
from datetime import datetime
import os
import socket

app = Flask(__name__)


# Function to calculate time difference between two timestamps
def calculate_time_difference(timestamp1, timestamp2):
    fmt = '%a %d %b %Y %H:%M:%S %z'
    time1 = datetime.strptime(timestamp1, fmt)
    time2 = datetime.strptime(timestamp2, fmt)
    diff = abs((time2 - time1).total_seconds())
    return diff


# Flask route to handle POST requests for time difference calculation
@app.route('/time_difference', methods=['POST'])
def time_difference_route():
    try:
        data = request.data.decode("utf-8").replace("\r", "")  # Strip carriage returns
        lines = data.strip().split('\n')
        count = int(lines[0])
        if count != len(lines) - 1:
            return jsonify({"error": "Not enough data"}), 400

        # Extract the timestamps
        timestamp1 = lines[1]
        timestamp2 = lines[2]

        # Calculate the time difference
        time_diff = calculate_time_difference(timestamp1, timestamp2)

        # Get node ID (hostname in this case)
        node_id = socket.gethostname()

        # Return the result with node ID
        return jsonify({"id": node_id, "result": [time_diff]})

    except Exception as e:
        return jsonify({"error": str(e)}), 400


# Entry point of the application
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
