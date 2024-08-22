import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import UnivariateSpline

def smoothing_spline_ts(ser, s_scale = 20, plot=True):
    """
    Apply smoothing splines to a time series DataFrame.

    Parameters:
    - df: pandas DataFrame with a datetime index.
    - value_col: String, name of the column to smooth.
    - s: Float, smoothing factor. Larger values result in smoother curves.
    - plot: Boolean, whether to plot the original and smoothed data.

    Returns:
    - spline: UnivariateSpline object for further use.
    - smoothed_df: pandas DataFrame with smoothed values.
    """
    # Ensure the index is a datetime index
    if not isinstance(ser.index, pd.DatetimeIndex):
        raise ValueError("The DataFrame index must be a DatetimeIndex.")
    
    x = ser.index
    y = ser
    
    # Convert datetime index to numeric for smoothing spline
    x_numeric = np.arange(len(x))
    dt_min = (x[1].timestamp() - x[0].timestamp()) / 60
    
    # Apply Smoothing Splines
    spline = UnivariateSpline(x_numeric, y, s=s_scale * len(x) / dt_min)
    
    # Create a DataFrame for the smoothed values
    smoothed_values = spline(x_numeric)
    smoothed = pd.Series(smoothed_values, index=x)
    
    # Plot results if desired
    if plot:
        plt.figure(figsize=(12, 6))
        plt.plot(ser.index,y, label='Original Data', linestyle='dotted', color='gray')
        plt.plot(smoothed.index, smoothed, label='Smoothing Spline', color='red')
        plt.legend()
        plt.title('Smoothing Splines')
        plt.xlabel('Time')
        plt.show()

    return smoothed