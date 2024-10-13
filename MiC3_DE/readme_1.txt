MiC3 Data Engineering Assessment - Problem Set 1
Author: Shashi Hagroo
Date: 12 October 2024

Time Difference Calculator API

This Flask application is a simple API to calculate the time difference between two timestamps. It accepts a POST request with the timestamps in a specified format and returns the time difference in seconds along with the node ID.

Components

    Calculates the absolute time difference between two provided timestamps.
    Returns the result as a JSON response.
    Uses Flask for easy routing and request handling.

Requirements

    Python 3.8 or higher
    Flask
    MarkupSafe
    ItsDangerous
    Jinja2
    Werkzeug

Installation

    Clone the repository:

    bash

git clone <repository_url>
cd <repository_name>

Create a virtual environment (optional but recommended):

python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`

Install the required packages:
    pip install -r requirements.txt

Usage
    Run the application:
	python app.py

The application will start and listen on port 5000.

Send a POST request to the API:
The request body should contain the following format:
<count_of_timestamps>
<timestamp1>
<timestamp2>

Example request:
2
Wed 12 Oct 2024 12:00:00 +0000
Wed 12 Oct 2024 15:00:00 +0000

Example of using curl:
curl -X POST http://localhost:5000/time_difference -d "2\nWed 12 Oct 2024 12:00:00 +0000\nWed 12 Oct 2024 15:00:00 +0000"

Response:
The API will return a JSON response with the time difference:
    {
        "id": "node_id",
        "result": [10800]
    }
    Here, 10800 is the time difference in seconds.

Docker Usage
    Build the Docker image:
docker build -t mic3_flask_app .

Run the Docker container:
    docker run -p 5000:5000 mic3_flask_app

Error Handling
In case of errors, the API will return a JSON response with an error message. For example:
{
    "error": "Not enough data"
}

