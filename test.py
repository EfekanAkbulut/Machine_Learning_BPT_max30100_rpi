import smbus

# Define the I2C address of the MAX30100 sensor.
MAX30100_ADDRESS = 0x57

# Initialize the I2C bus.
bus = smbus.SMBus(1)

# Reset the sensor.
bus.write_byte_data(MAX30100_ADDRESS, 0x09, 0x40)

# Read the sensor data.
while True:
    # Read the FIFO register.
    fifo_data = bus.read_i2c_block_data(MAX30100_ADDRESS, 0x07, 6)

    # Extract the heart-rate and SpO2 values from the FIFO data.
    hr = (fifo_data[3] << 8) | fifo_data[4]
    spo2 = fifo_data[5]

    # Print the heart-rate and SpO2 values.
    print("Heart-rate: %d bpm, SpO2: %d%%" % (hr, spo2))
