import serial
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from collections import deque
import time
import csv
from datetime import datetime

# Config
PORT = '/dev/ttyUSB0'
BAUD_RATE = 115200
WINDOW_SIZE = 500      # Number of live data points displayed at once
MAGNIFICATION = 3.5    # Gain multiplier to amplify peak height

try:
    ser = serial.Serial(PORT, BAUD_RATE, timeout=1)
    print(f"[SUCCESS] Connected to hardware on {PORT}")
except Exception as e:
    print("\n" + "="*60)
    print(f"[ERROR] Could not connect to hardware on port '{PORT}'.")
    print(f"Details: {e}")
    print("Please connect your ESP32 board and verify the port.")
    print("="*60 + "\n")
    exit()

filename = datetime.now().strftime("%Y%m%d%H%M%S") + "_heart_rate_reading.csv"
with open(filename, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(["Time_s", "Filtered_Amplitude"])

y_data = deque([0.0] * WINDOW_SIZE, maxlen=WINDOW_SIZE)
x_data = deque([0.0] * WINDOW_SIZE, maxlen=WINDOW_SIZE)
peak_times = []
start_time = time.time()

plt.style.use('dark_background')
fig, ax = plt.subplots(figsize=(10, 5))
fig.canvas.manager.set_window_title('ESP32 Live Heart Rate Monitor')

line, = ax.plot([], [], color='#00ff00', lw=1.8)
ax.set_ylabel("Amplitude (mV)", color='#00ff00', fontsize=11)
ax.set_xlabel("Time (s)", color='#00ff00', fontsize=11)
ax.grid(True, color='#222222', linestyle='--', linewidth=0.5)

bpm_text = ax.text(0.5, 0.93, 'BPM: --', transform=ax.transAxes,
                   color='red', fontsize=26, ha='center', va='top', weight='bold')

# animation loop
def update(frame):
    current_time = time.time() - start_time
    
    while ser.in_waiting > 0:
        try:
            line_str = ser.readline().decode('utf-8', errors='ignore').strip()
            if "Filtered:" in line_str:
                parts = line_str.split(',')
                for part in parts:
                    if "Filtered:" in part:
                        val = float(part.split(':')[1])
                        
                        # Subtract 2048 ADC baseline offset and apply software gain
                        processed_val = (val - 2048.0) * MAGNIFICATION
                        
                        x_data.append(current_time)
                        y_data.append(processed_val)
                        
                        # Log measurements directly to file
                        with open(filename, 'a', newline='') as f:
                            csv.writer(f).writerow([current_time, processed_val])
                        
                        # Peak detection: LOOK MORE INTO
                        if processed_val > 250:  # Threshold spike
                            if not peak_times or (current_time - peak_times[-1] > 0.4): # Debounce limit (~150 BPM)
                                peak_times.append(current_time)
                                
        except (ValueError, IndexError):
            pass

    if len(x_data) > 0:
        line.set_data(list(x_data), list(y_data))
        
        # Horizontal scrolling window
        ax.set_xlim(min(x_data), max(x_data))
        
        # Automatic Vertical Sizing (fits signals dynamically while supporting manual toolbar zooming)
        ymin, ymax = min(y_data), max(y_data)
        margin = max((ymax - ymin) * 0.2, 50.0)
        ax.set_ylim(ymin - margin, ymax + margin)

    # Calculate rolling BPM over the last 10 seconds of detected peaks
    recent_peaks = [p for p in peak_times if current_time - p <= 10.0]
    if len(recent_peaks) >= 2:
        intervals = [recent_peaks[i] - recent_peaks[i-1] for i in range(1, len(recent_peaks))]
        avg_interval = sum(intervals) / len(intervals)
        if avg_interval > 0:
            bpm = 30.0 / avg_interval
            bpm_text.set_text(f'BPM: {int(bpm)}')
    else:
        bpm_text.set_text('BPM: --')

    return line, bpm_text

# Run animation loop fed purely by incoming hardware data
ani = animation.FuncAnimation(fig, update, interval=20, blit=False, cache_frame_data=False)
plt.show()
