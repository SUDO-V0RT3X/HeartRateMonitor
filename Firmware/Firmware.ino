// ESP32 ECG Signal Reader & Software Filter
#define ECG_PIN 34          // Input pin connected to MCP6024 Pin 8 (VOUTC)
#define SAMPLE_INTERVAL 4  // Sample every 4 ms (250 Hz sampling rate)

unsigned long lastSampleTime = 0;

// Exponential Moving Average (EMA) Filter variables
float emaFilteredSignal = 2048.0; // Initialize at mid-scale (12-bit ADC mid = 2048)
const float alpha = 0.15;      // Smoothing factor (0 < alpha < 1). Lower = smoother

// 50 Hz Notch Filter tuned for a 250 Hz Sampling Rate
float notchFilter(float input) {
  static float x[3] = {0, 0, 0};
  static float y[3] = {0, 0, 0};
  
  x[0] = input;
  
  // Coefficient matrix to notch out exactly 50Hz at a 250Hz sample rate
  y[0] = 0.625 * x[0] - 0.386 * x[1] + 0.625 * x[2] + 0.386 * y[1] - 0.25 * y[2];
  
  // Shift the values for the next iteration
  x[2] = x[1]; x[1] = x[0];
  y[2] = y[1]; y[1] = y[0];
  
  return y[0];
}

void setup() {
  Serial.begin(115200);
  
  // Configure ADC resolution
  analogReadResolution(12);             // 0 to 4095
  analogSetAttenuation(ADC_11db);       // 0V to 3.3V range
  
  pinMode(ECG_PIN, INPUT);
}

void loop() {
  unsigned long currentMicros = micros();
  
  // Maintain a steady sampling rate of 250 Hz
  if (currentMicros - lastSampleTime >= (SAMPLE_INTERVAL * 1000)) {
    lastSampleTime = currentMicros;
    
    // Read the analog signal from the amplifier output
    int rawADC = analogRead(ECG_PIN);
    
    // 1. Apply the 50 Hz Digital Notch Filter first
    float notchedSignal = notchFilter((float)rawADC);
    
    // 2. Apply the Low-Pass Smoothing Filter (EMA) to the notched signal
    emaFilteredSignal = (alpha * notchedSignal) + ((1.0 - alpha) * emaFilteredSignal);
    
    // Output formatted for the Arduino Serial Plotter
    Serial.print("Raw:");
    Serial.print(rawADC);
    Serial.print(",");
    Serial.print("Filtered:");
    Serial.println((int)emaFilteredSignal);
  }
}