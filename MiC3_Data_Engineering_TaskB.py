# MiC3 Data Engineering Assessment - Problem Set 1 Task B
# 12 October 2024
# Author: Shashi Hagroo

from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)


def calculate_time_difference(timestamp1, timestamp2):
    from datetime import datetime

    # Parse the timestamps
    fmt = '%a %d %b %Y %H:%M:%S %z'
    time1 = datetime.strptime(timestamp1, fmt)
    time2 = datetime.strptime(timestamp2, fmt)

    # Calculate the difference in seconds
    diff = abs((time2 - time1).total_seconds())

    # Return the difference
    return diff


@app.route('/time_difference', methods=['POST'])
def time_difference():
    try:
        data = request.data.decode("utf-8").replace("\r", "")  # Strip carriage returns
        lines = data.strip().split('\n')
        count = int(lines[0])
        if count != len(lines) - 1:
            return jsonify({"error": "Not enough data"}), 400

        # Extract the timestamps
        timestamp1 = lines[1]
        timestamp2 = lines[2]

        # Calculate the difference
        time_diff = calculate_time_difference(timestamp1, timestamp2)

        return jsonify({"difference": time_diff})
    except Exception as e:
        return jsonify({"error": str(e)}), 400


if __name__ == '__main__':
    app.run(debug=True)

