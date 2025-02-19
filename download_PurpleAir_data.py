import numpy as np
import pandas as pd
import requests
from io import StringIO

def data_name(sensor_id, start_time, end_time):
    return f"{sensor_id}-{start_time}-{end_time}"

def get_purpleair_sensor_ids(api_key='8FF7CBA4-A704-11ED-B6F4-42010A800007'):
    url = "https://api.purpleair.com/v1/sensors"
    headers = {
        "X-API-Key": api_key
    }
    fields = ["sensor_index" ,"name", "location_type", "position_rating", "latitude", "longitude", "altitude", "confidence"]
    params = {
        "fields": ','.join(fields),
        # "location_type": int(indoor),  # 0 for outdoor sensors, 1 for indoor sensors
        "private": False,
    }
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code == 200:
        sensors = response.json()["data"]
        return pd.DataFrame(sensors, columns=fields)
    else:
        raise Exception(f"Error: {response.status_code} - {response.text}")

def fetch_purpleair_data(sensor_ids, start_stamp, end_stamp, path, api_key = '8FF7CBA4-A704-11ED-B6F4-42010A800007'):
    """
    API Documentation: https://api.purpleair.com/
    Community page: https://community.purpleair.com/c/data/
    """
    # Create empty dataframe and break timespan up into 2 day segments since this is the max the API allows
    url = "https://api.purpleair.com/v1/sensors"
    headers = {
        "X-API-Key": api_key
    }
    fields = ["pressure", "temperature", "humidity", "pm1.0_atm", "pm2.5_atm", "pm10.0_atm"]

    windows = np.arange(start_stamp, end_stamp, 47 * 3600, dtype=int)
    for sensor_id in sensor_ids:
        df = pd.DataFrame()
        for i in range(len(windows) - 1):
            params = {
                "fields": ','.join(fields),
                "average": 0,
                "start_timestamp": windows[i],
                "end_timestamp": windows[i+1],
            }
            response = requests.get(f"{url}/{sensor_id}/history/csv", headers=headers, params=params)
            if response.status_code != 200:
                raise Exception(f'Error querying data between {windows[i]} and {windows[i+1]}, status: {response.status_code}')

            df = pd.concat([df, pd.read_csv(StringIO(response.text))])

        # Sort by time and remove duplicates
        df.drop_duplicates(subset=['time_stamp', 'sensor_index'], inplace=True)
        df.sort_values(by='time_stamp', inplace=True)  # Sort by time
        df.reset_index(inplace=True)
        df.drop('index', axis=1, inplace=True)  # Delete old index column

        # Convert pressure to Pa
        df['pressure'] = df['pressure'] * 100

        # Remove sensor_index and export to Parquet
        # df = df[['time_stamp', 'sensor_index', 'pressure']].rename(columns={'time_stamp': 't', 'sensor_index': 'ID', 'pressure': 'P'})
        df.to_parquet(f"{path}/{data_name(sensor_id, start_stamp, end_stamp)}.parquet")

        print(f"Sensor {sensor_id} data exported for timespan {start_stamp} to {end_stamp}")
        print(f"{df.shape[0]} rows exported and saved")

def main():
    sensor_ids = [3218]#, 67467, 95397, 75899, 155155, 77859, 19477, 30559, 167279, 155745]  # Add more sensor IDs as needed
    start_stamp = 1671082090
    end_stamp = 1675238400
    path = './Data/Seattle_deployment_4_Dec-Jan'
    
    fetch_purpleair_data(sensor_ids, start_stamp, end_stamp, path)

if __name__ == "__main__":
    main()
