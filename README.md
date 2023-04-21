# Machine_Learning_BPT_max30100_rpi

The code is written in Python and is designed to interface a MAX30100 PPG sensor with a Raspberry Pi to capture PPG signals, filter the signals, and store the filtered signals in a CSV file. In addition, the code uses a machine learning model to predict blood pressure based on the filtered PPG signals, and saves the predicted blood pressure values to the same CSV file.

The MAX30100 PPG sensor is a device that can be used to detect changes in blood volume in order to measure heart rate and blood oxygen saturation. In this code, the PPG sensor is used to capture the PPG signals, which are essentially the changes in light absorption due to blood flow through the skin. The sensor is enabled to capture both the red and infrared light wavelengths.

Once the PPG signals are captured, they are filtered using a bandpass filter to remove noise and any unwanted frequencies. This filtering is performed using the butter and lfilter functions from the scipy.signal library. The filtered PPG signals are then stored in a CSV file using the csv.writer function.

In addition to capturing and filtering the PPG signals, the code also uses a machine learning model to predict blood pressure based on the filtered PPG signals. The machine learning model is loaded from a file using the joblib.load function from the sklearn.externals library, and a scaler object is loaded from another file using the same function from the sklearn.preprocessing library. These files should contain a trained machine learning model and a scaler object that were previously saved using the joblib.dump function.

The features for the machine learning model are computed using the mean and standard deviation of the filtered red and IR signals. These features are scaled using the scaler object that was loaded from the file. The machine learning model is then used to make a blood pressure prediction based on the scaled features.

Finally, the predicted systolic blood pressure (SBP) and diastolic blood pressure (DBP) values are printed to the console and written to the CSV file along with the filtered PPG signals. These values can be visualized and analyzed in a spreadsheet program like Microsoft Excel.

Overall, the code provides a way to capture PPG signals from a MAX30100 PPG sensor, filter the signals to remove noise, and use a machine learning model to predict blood pressure based on the filtered signals. The resulting data can be stored in a CSV file for further analysis and visualization.
