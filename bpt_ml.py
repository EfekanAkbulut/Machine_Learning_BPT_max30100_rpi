from max30100 import MAX30100
import time
import csv
from scipy.signal import butter, lfilter
from sklearn.externals import joblib
from sklearn.preprocessing import StandardScaler

sensor = MAX30100()

sensor.enable_spo2()

filename = "ppg_data.csv"
model_filename = "bp_model.pkl"
scaler_filename = "bp_scaler.pkl"

with open(filename, "w") as csv_file:
    writer = csv.writer(csv_file, delimiter=",")
    writer.writerow(["Red", "IR"])

    # Load the machine learning model and scaler
    model = joblib.load(model_filename)
    scaler = joblib.load(scaler_filename)

    while True:
        red, ir = sensor.read_sequential()

        # Filter the PPG signals
        lowcut = 0.5  # Lower cutoff frequency (Hz)
        highcut = 10.0  # Upper cutoff frequency (Hz)
        fs = 100.0  # Sampling rate (Hz)
        nyquist = 0.5 * fs
        low = lowcut / nyquist
        high = highcut / nyquist
        order = 2
        b, a = butter(order, [low, high], btype="band")
        red_filtered = lfilter(b, a, red)
        ir_filtered = lfilter(b, a, ir)

        # Compute the features for the machine learning model
        features = [red_filtered.mean(), red_filtered.std(), ir_filtered.mean(), ir_filtered.std()]
        features_scaled = scaler.transform([features])

        # Make a blood pressure prediction using the machine learning model
        sbp, dbp = model.predict(features_scaled)[0]

        print("SBP: {0}, DBP: {1}".format(sbp, dbp))
        writer.writerow([red_filtered, ir_filtered, sbp, dbp])
        time.sleep(0.1)
