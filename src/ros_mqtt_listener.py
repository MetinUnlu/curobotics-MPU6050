#!/usr/bin/env python

import time        #import
import math
import struct
import rospy
from sensor_msgs.msg import Imu
import paho.mqtt.client as mqtt
import numpy as np
import pandas as pd


MQTT_ADDRESS = '192.168.1.104'
MQTT_USER = 'lastingk'
MQTT_PASSWORD = '1234'
MQTT_TOPIC = 'main/+/+'

IMU_FRAME=None


def on_connect(client, userdata, flags, rc):
    """ The callback for when the client receives a CONNACK response from the server."""
    print('Connected with result code ' + str(rc))
    client.subscribe(MQTT_TOPIC)

def on_message(client, userdata, msg):
    acceleration_x=0
    acceleration_y=0
    acceleration_z=0
    gyro_x=0
    gyro_y=0
    gyro_z=0
    
    imu_msg=Imu()
    imu_msg.header.frame_id = IMU_FRAME	
    imu_pub=rospy.Publisher('imu/data_raw', Imu, queue_size=10)
    """The callback for when a PUBLISH message is received from the server."""
    datalist=str(msg.payload)
    datalist=datalist.strip("b")
    datalist=datalist.strip("'")
    datalist=datalist.split(',')

    acceleration_x=float(datalist[0])
    acceleration_y=float(datalist[1])
    acceleration_z=float(datalist[2])
    gyro_x=float(datalist[3])
    gyro_y=float(datalist[4])
    gyro_z=float(datalist[5])

    imu_msg.linear_acceleration.x=acceleration_x
    imu_msg.linear_acceleration.y=acceleration_y
    imu_msg.linear_acceleration.z=acceleration_z
    
    imu_msg.angular_velocity.x=gyro_x
    imu_msg.angular_velocity.y=gyro_y
    imu_msg.angular_velocity.z=gyro_z

    imu_pub.publish(imu_msg)
    #print(time.time()) 
    print("Accelerations: ", acceleration_x, ", ",acceleration_y, ", ", acceleration_z, "  Gyros: ", gyro_x, ", ", gyro_y, ", ", gyro_z)
    imu_msg.header.stamp=rospy.Time.now()	

imu_pub=None

def MQTTbroker():

    rospy.init_node('MQTT_Broker')
    IMU_FRAME=rospy.get_param('~imu_frame', 'imu_link')
    mqtt_client = mqtt.Client()
    mqtt_client.username_pw_set(MQTT_USER, MQTT_PASSWORD)
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message
    mqtt_client.connect(MQTT_ADDRESS, 1883)
    mqtt_client.loop_start()
    rospy.spin()
    




if __name__ == '__main__':
    try:
        MQTTbroker()
    except rospy.ROSInterruptException:
        pass
