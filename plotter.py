import serial
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from collections import deque

PORT = '/dev/ttyUSB0'  
BAUD_RATE = 115200
WINDOW_SIZE = 1000    
MAGNIFICATION = 10.0  

try:
    ser = serial.Serial(PORT, BAUD_RATE, timeout=1)
except Exception as e:
    print(f"Error opening serial port: {e}")
    print("Make sure the Arduino Serial Plotter/Monitor is CLOSED!")
    exit()

# Store magnified values
y_data = deque([2048 * MAGNIFICATION] * WINDOW_SIZE, maxlen=WINDOW_SIZE)

plt.style.use('dark_background')
fig, ax = plt.subplots(figsize=(10, 4))
fig.canvas.manager.set_window_title('Heart Rate Monitor')

line, = ax.plot(y_data, color='#00ffcc', linewidth=2)
ax.set_title("Heart Rate Monitor", color='#00ffcc', fontsize=16)
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
                        # Apply magnification directly without assuming a perfect 2048 baseline
                        y_data.append(raw_val * MAGNIFICATION)
                        
        except (ValueError, UnicodeDecodeError, IndexError):
            pass 
            
    line.set_ydata(y_data)
    
    # TRACKING CAMERA: Find the actual center of the current data
    if len(y_data) > 0:
        current_center = sum(y_data) / len(y_data)
        
        # Keep a fixed "magnifying glass" window size (+/- 4000) so noise remains stable,
        # but let the window slide up or down to follow the true baseline.
        ax.set_ylim(current_center - 4000, current_center + 4000)
        
    return line,

ani = animation.FuncAnimation(fig, update, interval=20, blit=False, cache_frame_data=False)
plt.show()
