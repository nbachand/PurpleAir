import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection

def plot_colored_line(fig, ax, ser, color_values, colormap='brg'):
    """
    Plot a line with color changing based on a second array.

    Parameters:
    - x: Array of x-values.
    - y: Array of y-values.
    - color_values: Array of values used to determine the color of the line segments.
    - colormap: Optional colormap name.

    Returns:
    - None
    """
    # Ensure x, y, and color_values are numpy arrays
    x = ser.index.astype(int).values
    y = ser.values
    x = np.asarray(x)
    y = np.asarray(y)
    color_values = np.asarray(color_values)
    
    # Create line segments
    points = np.array([x, y]).T.reshape(-1, 1, 2)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)
    
    # Normalize color values
    norm = plt.Normalize(color_values.min(), color_values.max())
    cmap = plt.get_cmap(colormap)
    
    # Create a LineCollection object
    lc = LineCollection(segments, colors=cmap(norm(color_values)), linewidth=1)
    
    # Plot
    ax.add_collection(lc)
    ax.autoscale()
    # ax.set_xlim(x.min(), x.max())
    # ax.set_ylim(y.min(), y.max())

    # Add colorbar manually
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    cbar = fig.colorbar(sm, ax=ax, orientation='horizontal')
    cbar.set_label('Color scale based on second array')
    
    return fig, ax