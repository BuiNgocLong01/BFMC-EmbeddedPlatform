# BFMC Competition: Save Data

import cv2
import time
import csv
import os
import serial
from datetime import datetime

# Set FPS
desired_fps = 20  

# connect to STM32 Nucleo (Serial port)
arduino_port = 'COM3'  
baud_rate = 9600  # baudrate
arduino = serial.Serial(arduino_port, baud_rate)
time.sleep(2) 

# Init video capture
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    raise IOError("dont open webcam")

# Create output folder
output_dir = "output_img"
os.makedirs(output_dir, exist_ok=True)

# save data to csv
csv_file = "dataInput.csv"
fieldnames = ['image_path', 'data1', 'data2']
# fieldnames = ['timestamp','image_path', 'data1', 'data2']

# Ghi header vào file CSV
with open(csv_file, mode='w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()

start_time = time.time()
frame_id = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break

    current_time = time.time()
    if (current_time - start_time) >= 1/desired_fps:
        # read data from arduino
        if arduino.in_waiting:
            line = arduino.readline().decode('utf-8').strip()
            data1, data2 = line.split(',')  # data frame received: "data1,data2"

            # save img
            image_path = os.path.join(output_dir, f"frame_{frame_id}.jpg")
            cv2.imwrite(image_path, frame)
            
            # Write data to csv
            with open(csv_file, mode='a', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                # writer.writerow({'timestamp': datetime.now(), 'image_path': image_path, 'data1': data1, 'data2': data2})
                writer.writerow({'image_path': image_path, 'data1': data1, 'data2': data2})
                print('Da luu !')

            frame_id += 1
            start_time = current_time

    cv2.imshow('Webcam', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Destroy
cap.release()
cv2.destroyAllWindows()
arduino.close()
