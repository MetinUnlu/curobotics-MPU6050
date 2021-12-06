# curobotocis
MPU 6050 With Kalman Filter using ROS Wifi Communication

This repository contains IMU Motion analysis related codes for a project work of Cukurova Robotics Lab.

For collecting sensor data, NodeMCUv3 card is used.

As arduino code, Adafruit's basic data reading is used since we only need basic data at this point, filter will be done in ROS.
To get raw data from Adafruit, scaling should be removed from "Adafruit_MPU6050.cpp".

The arduino code in repository is edited in order to get basic IMU data broadcast in MQTT server. Thus from MQTT communication we can receieve this data and published in ROS with "sensor_msgs.msg/Imu" under "imu/data_raw " topic.

By subscribing to "imu/data_raw", calibration, scaling and any desired filter methods can be used. For simplicity, offset and scaling can be applied to this data in seperate node, which "imu_streamer.py" file does. This node will publish the data in "imu/data" for the usage of nodes containing filter algorithms.

In this repository kalman filter is applied to get accurate orientation data in X and Y axis of MPU6050.



