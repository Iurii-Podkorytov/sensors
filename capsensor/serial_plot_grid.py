import serial
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import Normalize
import matplotlib.cm as cm

# Initialize serial connection
ser = serial.Serial('COM7', 9600, timeout=1)

# Function to parse the incoming data
def parse_data(line):
    """
    Parse the input string into a dictionary of pin: value pairs.
    Example input: "pin2:12,pin3:15,pin4:10,..."
    """
    data = {}
    parts = line.strip().split(',')
    for part in parts:
        if ':' in part:
            pin, value = part.split(':')
            try:
                data[pin] = int(value)
            except ValueError:
                pass  # Ignore invalid values
    return data

# Initialize the plot
fig, ax = plt.subplots(figsize=(6, 6))  # Create a square figure
plt.ion()  # Turn on interactive mode for dynamic plotting

# Function to update the plot
def update_plot(grid_values):
    """
    Update the 3x3 grid plot with the given values.
    """
    ax.clear()  # Clear the current plot

    # Create a 3x3 grid
    grid = np.zeros((3, 3))

    # Map the pin numbers to their respective grid positions
    pin_to_grid = {
        'pin2': (0, 0), 'pin3': (0, 1), 'pin4': (0, 2),
        'pin5': (1, 0), 'pin6': (1, 1), 'pin7': (1, 2),
        'pin8': (2, 0), 'pin9': (2, 1), 'pin10': (2, 2)
    }

    # Populate the grid with the values
    for pin, value in grid_values.items():
        if pin in pin_to_grid:
            x, y = pin_to_grid[pin]
            grid[x, y] = value

    # Normalize the values for color mapping
    norm = Normalize(vmin=0, vmax=1000)  # Adjust vmax based on expected values
    colors = cm.viridis(norm(grid))  # Use the 'viridis' colormap

    # Plot the grid as a square with proper alignment
    ax.imshow(colors, extent=[0, 3, 0, 3], origin='upper', aspect='equal')

    # Add text labels for values, centered within each square
    for i in range(3):
        for j in range(3):
            ax.text(j + 0.5, 2.5 - i, f"{grid[i, j]:.0f}", 
                    ha='center', va='center', color='white', fontsize=12)

    # Set axis limits and remove ticks
    ax.set_xlim(0, 3)
    ax.set_ylim(0, 3)
    ax.set_xticks([])
    ax.set_yticks([])

    # Draw the grid lines between the squares
    for i in range(4):  # Draw 4 vertical and 4 horizontal lines
        ax.axvline(i, color='black', linewidth=2)
        ax.axhline(i, color='black', linewidth=2)

    # Redraw the plot
    fig.canvas.draw_idle()
    plt.pause(0.001)  # Pause to allow the plot to update

# Main loop
if __name__ == "__main__":
    print("Listening for data on COM7...")

    while True:
        try:
            # Read a line from the serial port with error handling
            line = ser.readline().decode('utf-8', errors='replace').strip()
            if line:
                # Parse the data
                data = parse_data(line)
                # Update the plot
                update_plot(data)
        except KeyboardInterrupt:
            print("Exiting...")
            break

    ser.close()  # Close the serial connection when done