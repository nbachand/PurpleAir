import numpy as np
import pandas as pd
import requests
from io import StringIO
import scipy.io as sio

#===============================================================
# sensor_id = 3218 
sensor_ids = [3218, 67467, 95397, 75899, 155155, 77859, 19477, 30559, 167279, 155745]

# start_time = 1652156890
# end_time = 1656649690
# path = '../Data/Seattle_deployment_2_May-July'

start_time = 1671082090
end_time = 1675238400
path = '../Data/Seattle_deployment_4_Dec-Jan'
#===============================================================

# Create empty dataframe and break timespan up into 2 day segments since this
# is the max the api allows
df = pd.DataFrame(columns=['time_stamp', 'sensor_index', 'pressure'])
windows = np.arange(start_time, end_time, 47*3600, dtype=int)
for id in sensor_ids:
    for i in range(len(windows) - 1):
        response = requests.get(
            "https://api.purpleair.com/v1/sensors/" + str(id) + "/history/csv?start_timestamp=" + str(windows[i]) + "&end_timestamp=" + str(windows[i+1]) + "&average=0&fields=pressure",
            headers={'X-API-Key' : '8FF7CBA4-A704-11ED-B6F4-42010A800007'}
        )
        if response.status_code != 200:
            raise Exception('Error querying data between ' + str(windows[i]) + ' and ' + str(windows[i+1]) + ' , status: ' + str(response.status_code))
        df = pd.concat([df, pd.read_csv(StringIO(response.text))])

# Sort by time and remove duplicates:
df.drop_duplicates(subset=['time_stamp', 'sensor_index'], inplace=True)
df.sort_values(by='time_stamp', inplace=True) # sort by time
df.reset_index(inplace=True)
df.drop('index', axis=1, inplace=True) # delete old index column

# Convert pressure to Pa:
df['pressure'] = df['pressure'] * 100

# Remove sensor_index and export to MATLAB:
df = df[['time_stamp', 'sensor_index', 'pressure']].rename(columns={'time_stamp' : 't', 'sensor_index' : 'ID', 'pressure' : 'P'})
sio.savemat(path + '/PurpleAir_new.mat', {'PurpleAir':df.to_dict("list")})

print(str(df.shape[0]) + ' rows exported and saved')