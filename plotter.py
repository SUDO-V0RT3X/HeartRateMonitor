import serial
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from collections import deque

PORT = '/dev/ttyUSB0'  
BAUD_RATE = 115200
WINDOW_SIZE = 1000    # REDUCED: 500 points creates a readable 2-second moving window
MAGNIFICATION = 5.0  # ADDED: Multiplier to stretch the height of the waveform

try:
    ser = serial.Serial(PORT, BAUD_RATE, timeout=1)
except Exception as e:
    print(f"Error opening serial port: {e}")
    print("Make sure the Arduino Serial Plotter/Monitor is CLOSED!")
    exit()

# Centered at 0 instead of 2048
y_data = deque([0] * WINDOW_SIZE, maxlen=WINDOW_SIZE)

# --- SETUP MEDICAL MONITOR STYLING ---
plt.style.use('dark_background')
fig, ax = plt.subplots(figsize=(10, 4))
fig.canvas.manager.set_window_title('Heart Rate Monitor')

# Draw a neon green line for the signal
line, = ax.plot(y_data, color='#00ffcc', linewidth=2)

ax.set_title("Live ECG Trace", color='#00ffcc', fontsize=16)
ax.axis('off')  

def update(frame):
    while ser.in_waiting > 0:
        try:
            line_str = ser.readline().decode('utf-8').strip()
            
            if "Filtered:" in line_str:
                parts = line_str.split(',')
                for part in parts:
                    if "Filtered:" in part:
                        raw_val = int(part.split(':')[1])
                        
                        # SCALING MATH: Subtract the ESP32 baseline offset and apply gain
                        processed_val = (raw_val - 2048) * MAGNIFICATION
                        y_data.append(processed_val)
                        
        except (ValueError, UnicodeDecodeError, IndexError):
            pass 
            
    line.set_ydata(y_data)
    
    # DYNAMIC SCALING: Automatically zoom the Y-axis to frame the current data points perfectly
    if len(y_data) > 0:
        ymin, ymax = min(y_data), max(y_data)
        padding = max((ymax - ymin) * 0.2, 100) # Leave 20% margin above and below
        ax.set_ylim(ymin - padding, ymax + padding)
        
    return line,

# Run the animation loop at ~50fps (20ms interval)
ani = animation.FuncAnimation(fig, update, interval=20, blit=False, cache_frame_data=False)
plt.show()
