# MiC3 Data Engineering Assessment - Problem Set 2
# 13 October 2024
# Author: Shashi Hagroo

import pandas as pd
import numpy as np

# Data Load
df = pd.read_csv('ipdr.csv')

# Accounting for starttime and endtime data formats and converting to datetime
df['starttime'] = df['starttime'].str.replace(r'(\d{4}-\d{2}-\d{2})(\d{2}:\d{2}:\d{2})', r'\1 \2', regex=True)
df['endtime'] = df['endtime'].str.replace(r'(\d{4}-\d{2}-\d{2})(\d{2}:\d{2}:\d{2})', r'\1 \2', regex=True)

df['ST'] = pd.to_datetime(df['starttime'], errors='coerce', format='%Y-%m-%d %H:%M:%S')
df['ET'] = pd.to_datetime(df['endtime'], errors='coerce', format='%Y-%m-%d %H:%M:%S')

# Defining start and end times for filtering
start_time = df['ST'].min()
end_time = df['ET'].max()

# print(f"Min ST: {df['ST'].min()}, Max ST: {df['ST'].max()}")
# print(f"Min ET: {df['ET'].min()}, Max ET: {df['ET'].max()}")

# Formatting msisdn and domain to strings and removing any extra spaces
df['msisdn'] = df['msisdn'].astype(str).str.strip()
msisdns = df['msisdn'].unique()
df['domain'] = df['domain'].astype(str).str.strip()
domains = df['domain'].unique()

# Filtering the entire DataFrame by start_time and end_time
time_filtered_df = df[(df['ST'] >= start_time) & (df['ET'] <= end_time)]

# print(f"Total rows in the time range: {len(time_filtered_df)}")
# print(time_filtered_df[['msisdn', 'domain', 'ST', 'ET']].head())

# Iterating through each msisdn and domain in the filtered time range
for msisdn in msisdns:
    for domain in domains:
        # Filtering the time-filtered data for each msisdn and domain
        filtered_df = time_filtered_df[(time_filtered_df['msisdn'] == msisdn) & (time_filtered_df['domain'] == domain)]

        # Checking if there are any records left after filtering
        if not filtered_df.empty:
            print(f"Filtered data for MSISDN: {msisdn}, Domain: {domain}")
            print(filtered_df[['msisdn', 'domain', 'ST', 'ET']])

# Grouping data by domain to identify each VoIP app's calls
voip_calls = df.groupby('domain').agg({
    'ST': 'min',  # Minimum start time
    'ET': 'max',  # Maximum end time
    'msisdn': 'count'
}).reset_index()
voip_calls.rename(columns={'msisdn': 'msisdn_count'}, inplace=True)
print(voip_calls)

# Adding a new column for ET* which is ET minus 10 minutes
voip_calls['ET*'] = voip_calls['ET'] - pd.Timedelta(minutes=10)

# Calculating ET*(ET-10 min) for each FDR (idle time for each call)
# Create a new column that calculates the duration of each call after excluding the idle time [minutes].
voip_calls['Duration After Idle Time'] = (voip_calls['ET*'] - voip_calls['ST']).dt.total_seconds() / 60
print(voip_calls[['domain', 'ST', 'ET', 'ET*', 'Duration After Idle Time']])

# Adjusting ET based on the condition ET - 10 min < ST
voip_calls['Adjusted ET'] = np.where((voip_calls['ET'] - pd.Timedelta(minutes=10)) < voip_calls['ST'],
                                      voip_calls['ET'],
                                      voip_calls['ET*'])
print(voip_calls[['domain', 'ST', 'ET', 'ET*', 'Adjusted ET']])

# Grouping by 'domain' and calculating total volume from the original DataFrame
total_volume_per_domain = df.groupby('domain').agg(
    Total_DL_Volume=('ulvolume', 'sum'),  # Sum of upload volume
    Total_UL_Volume=('dlvolume', 'sum')   # Sum of download volume
).reset_index()

# Calculating Total Volume (DL + UL) in Bytes
total_volume_per_domain['Total_Volume_Bytes'] = total_volume_per_domain['Total_DL_Volume'] + total_volume_per_domain['Total_UL_Volume']

# Converting the total volume from Bytes to Kb
total_volume_per_domain['Total_Volume_Kb'] = total_volume_per_domain['Total_Volume_Bytes'] / 1024

# Drop the original bytes columns
total_volume_per_domain = total_volume_per_domain.drop(columns=['Total_DL_Volume', 'Total_UL_Volume'])
print(total_volume_per_domain)


# Calculating Highest ET* and Lowest ST for each domain
call_times = voip_calls.groupby('domain').agg(
    Highest_ET_star=('ET*', 'max'),
    Lowest_ST=('ST', 'min')
).reset_index()

# Calculating Total time of each call in seconds
call_times['Total_Call_Time_sec'] = (call_times['Highest_ET_star'] - call_times['Lowest_ST']).dt.total_seconds()
print(call_times[['domain', 'Highest_ET_star', 'Lowest_ST', 'Total_Call_Time_sec']])


# Merging the call times with total volume per domain
bitrate_data = call_times.merge(total_volume_per_domain,
                                 on='domain',
                                 how='left')

# Calculating Bit Rate in kbps
bitrate_data['Bit_Rate_kbps'] = (bitrate_data['Total_Volume_Kb'] * 1024) / bitrate_data['Total_Call_Time_sec']
print(bitrate_data[['domain', 'Total_Volume_Kb', 'Total_Call_Time_sec', 'Bit_Rate_kbps']])


# Discarding calls with Bit Rate < 10 kbps
filtered_calls = bitrate_data[bitrate_data['Bit_Rate_kbps'] >= 10].copy()

# Classifying calls based on Bit Rate


def classify_call(row):
    if row['Bit_Rate_kbps'] <= 200:
        return 'Audio Call'
    else:
        return 'Video Call'


# Applying the classification function to create a new column 'Call_Type'
filtered_calls.loc[:, 'Call_Type'] = filtered_calls.apply(classify_call, axis=1)  # Use .loc for assignment

# Counting Audio and Video Calls for each VoIP App
call_counts = filtered_calls.groupby(['domain', 'Call_Type']).size().reset_index(name='Count')
print(call_counts)
