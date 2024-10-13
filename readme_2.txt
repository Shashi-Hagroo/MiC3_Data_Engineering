MiC3 Data Engineering Assessment - Problem Set 2
Author: Shashi Hagroo
Date: 13 October 2024

This script processes call data from a CSV file (ipdr.csv) containing VoIP application records. The goal is to analyze the call data, calculate relevant metrics, and classify calls as either audio or video based on their bitrate.

Process

    Data Loading and Formatting:
        Load the dataset using pandas and parse the start time (starttime) and end time (endtime) columns into datetime format.
        Convert the msisdn and domain columns to strings and remove extra spaces.

    Time Filtering:
        Identify the minimum start time (ST) and maximum end time (ET) from the dataset.
        Filter the DataFrame to include only records within the identified time range.

    Grouping by Domain:
        Group the filtered data by domain to aggregate the following metrics:
            The minimum start time (ST) of calls.
            The maximum end time (ET) of calls.
            The count of calls (msisdn).

    Calculating Call Durations:
        Add a new column ET* representing the end time minus 10 minutes.
        Calculate the duration of each call after excluding idle time.
        Adjust the ET value based on whether it falls within the defined conditions.

    Calculating Total Volume:
        Group the original DataFrame by domain to calculate total upload and download volumes.
        Combine these to get the total volume in bytes, then convert to kilobytes (Kb).

    Calculating Call Times:
        Calculate the highest ET* and lowest ST for each domain.
        Determine the total call time in seconds by subtracting the lowest ST from the highest ET*.

    Bitrate Calculation:
        Merge the call times with total volume data.
        Calculate the bitrate for each call in kilobits per second (kbps).

    Filtering Calls:
        Discard calls with a bitrate of less than 10 kbps.
        Classify the remaining calls as either "Audio Call" or "Video Call" based on their bitrate:
            Calls with a bitrate of 200 kbps or less are classified as "Audio Calls."
            Calls with a bitrate greater than 200 kbps are classified as "Video Calls."

    Counting Call Types:
        Count the number of audio and video calls for each VoIP app (domain) and store the results.

Output

    The script prints the following data at various stages:
        Filtered VoIP call data by msisdn and domain.
        Summary of call metrics grouped by domain.
        Total volume calculations per domain.
        Call time calculations.
        Bitrate calculations.
        Final counts of audio and video calls.

Requirements

    Python 3.x
    Pandas library (pip install pandas)

Running the Script

Ensure that the ipdr.csv file is in the same directory as this script. Run the script using a Python environment.

python MiC3_Problem2.py

