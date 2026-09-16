import serial
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from collections import deque

# --- CONFIGURATION ---
# IMPORTANT: Change 'COM3' to the exact port your ESP32 is using (e.g., 'COM5' on Windows or '/dev/cu.usbserial...' on Mac)
PORT = '/dev/ttyUSB0'  
BAUD_RATE = 115200
WINDOW_SIZE = 500  # Number of data points to show on the screen at once

# --- SETUP SERIAL PORT ---
try:
    ser = serial.Serial(PORT, BAUD_RATE, timeout=1)
except Exception as e:
    print(f"Error opening serial port: {e}")
    print("Make sure the Arduino Serial Plotter/Monitor is CLOSED!")
    exit()

# Data storage array filled with the ESP32's mid-scale resting baseline
y_data = deque([2048] * WINDOW_SIZE, maxlen=WINDOW_SIZE)

# --- SETUP MEDICAL MONITOR STYLING ---
plt.style.use('dark_background')
fig, ax = plt.subplots(figsize=(10, 4))
fig.canvas.manager.set_window_title('ESP32 ECG')

# Draw a neon green line for the signal
line, = ax.plot(y_data, color='#00ffcc', linewidth=2)

# Lock the Y-axis to the ESP32's 12-bit ADC range (0 to 4095)
ax.set_ylim(0, 4095)
ax.set_title("Live ECG Monitor", color='#00ffcc', fontsize=16)
ax.axis('off')  # Hide the axes and grid for a clean hospital monitor look

def update(frame):
    while ser.in_waiting > 0:
        try:
            # Read a line from the ESP32
            line_str = ser.readline().decode('utf-8').strip()
            
            # Look for our formatted string: "Raw:123,Filtered:456"
            if "Filtered:" in line_str:
                parts = line_str.split(',')
                for part in parts:
                    if "Filtered:" in part:
                        # Extract the integer value after the colon
                        val = int(part.split(':')[1])
                        y_data.append(val)
        except (ValueError, UnicodeDecodeError, IndexError):
            # Ignore garbled serial data that often happens on startup
            pass 
            
    # Update the graph with the new data
    line.set_ydata(y_data)
    return line,

# Run the animation loop at ~50fps (20ms interval)
ani = animation.FuncAnimation(fig, update, interval=20, blit=True, cache_frame_data=False)
plt.show()
