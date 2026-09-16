import serial
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from collections import deque

# --- CONFIGURATION ---
PORT = '/dev/ttyUSB0'  # Update to your Linux port if needed (e.g. /dev/ttyACM0)
BAUD_RATE = 115200
WINDOW_SIZE = 500      # Number of data points visible on screen at once
MAGNIFICATION = 3.5    # Increase this number to make the peaks taller

# --- SETUP SERIAL PORT ---
try:
    ser = serial.Serial(PORT, BAUD_RATE, timeout=1)
except Exception as e:
    print(f"Error opening serial port: {e}")
    print("Make sure no other program is using the port!")
    exit()

# Data storage array initialized to 0 (centered baseline)
y_data = deque([0] * WINDOW_SIZE, maxlen=WINDOW_SIZE)

# --- SETUP MEDICAL MONITOR STYLING ---
plt.style.use('dark_background')
fig, ax = plt.subplots(figsize=(10, 4))
fig.canvas.manager.set_window_title('ESP32 ECG Monitor')

# Red trace matching your reference image style
line, = ax.plot(y_data, color='#ff4d4d', linewidth=1.5)

# Lock the Y-axis from -600 to +600 (matching your reference image)
ax.set_ylim(-600, 600)
ax.set_title("Live ECG Waveform", color='#ff4d4d', fontsize=14)
ax.grid(True, color='#333333', linestyle='--', linewidth=0.5)

def update(frame):
    while ser.in_waiting > 0:
        try:
            line_str = ser.readline().decode('utf-8').strip()
            if "Filtered:" in line_str:
                parts = line_str.split(',')
                for part in parts:
                    if "Filtered:" in part:
                        val = float(part.split(':')[1])
                        
                        # 1. Subtract 2048 baseline to shift center to 0
                        # 2. Multiply by MAGNIFICATION to stretch the peaks
                        processed_val = (val - 2048.0) * MAGNIFICATION
                        
                        y_data.append(processed_val)
        except (ValueError, UnicodeDecodeError, IndexError):
            pass 
            
    line.set_ydata(y_data)
    return line,

ani = animation.FuncAnimation(fig, update, interval=20, blit=True, cache_frame_data=False)
plt.show()
