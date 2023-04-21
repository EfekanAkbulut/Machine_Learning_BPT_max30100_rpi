import time
import csv
import numpy as np
import pandas as pd
import joblib
from scipy.signal import butter, lfilter
from sklearn.externals import joblib
from sklearn.preprocessing import StandardScaler
from Adafruit_CircuitPython_MAX30100 import MAX30100, HeartRate

# Initialize MAX30100 PPG sensor
max30100 = MAX30100()
max30100.enable_spo2()
max30100.set_mode(MAX30100.HEART_RATE_MODE)

# Define bandpass filter parameters
fs = 100  # Sampling frequency
lowcut = 0.5  # Low cutoff frequency
highcut = 5.0  # High cutoff frequency
order = 2  # Filter order

# Load machine learning model and scaler object
model = joblib.load('model.pkl')
scaler = joblib.load('scaler.pkl')

# Define CSV file name and header
filename = 'ppg_data.csv'
header = ['IR', 'R', 'SBP', 'DBP']

# Open CSV file and write header
with open(filename, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(header)

# Start data capture loop
while True:
    # Read PPG data
    ir, r = max30100.read_sequential()
    
    # Apply bandpass filter to PPG signals
    nyquist = 0.5 * fs
    low = lowcut / nyquist
    high = highcut / nyquist
    b, a = butter(order, [low, high], btype='band')
    ir_filt = lfilter(b, a, ir)
    r_filt = lfilter(b, a, r)
    
    # Compute features for machine learning model
    ir_mean = np.mean(ir_filt)
    ir_std = np.std(ir_filt)
    r_mean = np.mean(r_filt)
    r_std = np.std(r_filt)
    features = np.array([[ir_mean, ir_std, r_mean, r_std]])
    
    # Scale features using scaler object
    scaled_features = scaler.transform(features)
    
    # Make blood pressure prediction using machine learning model
    sbp, dbp = model.predict(scaled_features)[0]
    
    # Print predicted blood pressure values to console
    print('SBP:', sbp)
    print('DBP:', dbp)
    
    # Append filtered PPG signals and blood pressure values to CSV file
    with open(filename, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([ir_filt[-1], r_filt[-1], sbp, dbp])
    
    # Wait for next data capture cycle
    time.sleep(1)
