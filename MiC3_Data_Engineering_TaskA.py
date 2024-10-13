# MiC3 Data Engineering Assessment - Problem Set 1 Task A
# 12 October 2024
# Author: Shashi Hagroo

from datetime import datetime

def calculate_time_difference(t1, t2):
    time_format = "%a %d %b %Y %H:%M:%S %z"  # Define the time format inside the function
    dt1 = datetime.strptime(t1, time_format)
    dt2 = datetime.strptime(t2, time_format)
    time_diff = abs((dt1 - dt2).total_seconds())
    return int(time_diff)

# Take input from the user
T = int(input("Enter number of test cases: "))  # Number of test cases

for _ in range(T):
    t1 = input("Enter the first timestamp: ")
    t2 = input("Enter the second timestamp: ")
    print(calculate_time_difference(t1, t2))
