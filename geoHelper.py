import pandas as pd
from geopy.distance import great_circle

# Function to calculate distance
def is_within_radius(sensor_lat, sensor_lon, center_lat, center_lon, radius):
    if pd.isna(sensor_lat) or pd.isna(sensor_lon):
        return False
    distance = great_circle((center_lat, center_lon), (sensor_lat, sensor_lon)).meters
    return distance <= radius

import pandas as pd
from geopy.distance import great_circle

def find_closest_rows(df, target_index, n=1, location_type_value=0, lat_col='latitude', lon_col='longitude', location_type_col='location_type'):
    """
    Find the indices of the n closest rows in the DataFrame to the latitude and longitude of a given target index.
    Filters rows based on the location_type value.

    Parameters:
    - df: The DataFrame containing latitude and longitude columns.
    - target_index: The index of the row that provides the latitude and longitude to compare against.
    - n: Number of closest rows to return (default is 1).
    - location_type_value: The value of the location_type column to filter on (default is 0).
    - lat_col: The name of the column containing latitude values (default is 'latitude').
    - lon_col: The name of the column containing longitude values (default is 'longitude').
    - location_type_col: The name of the column containing location_type values (default is 'location_type').

    Returns:
    - List of indices of the n closest rows to the latitude and longitude of the target index.
    """
    # Retrieve the latitude and longitude from the target index
    center_lat = df.loc[target_index, lat_col]
    center_lon = df.loc[target_index, lon_col]
    
    # Filter DataFrame to only include rows where location_type equals location_type_value
    filtered_df = df[df[location_type_col] == location_type_value]
    
    # Calculate distances from the target coordinates to each row in the filtered DataFrame
    distances = filtered_df.apply(lambda row: great_circle((center_lat, center_lon), (row[lat_col], row[lon_col])).meters, axis=1)
    
    # Get the indices of the n closest rows
    closest_indices = distances.nsmallest(n).index.tolist()
    
    return closest_indices
