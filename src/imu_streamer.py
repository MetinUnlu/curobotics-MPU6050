#!/usr/bin/env python

import rospy
import math
from sensor_msgs.msg import Imu
import pandas as pd
from datetime import datetime

df=pd.DataFrame(columns=["accx","accy","accz","gyrox","gyroy","gyroz"])

IMU_FRAME=None
gravity_standart=9.806665
dps_to_rps=0.017453293
accx_offset=-61.1
accy_offset=-35.805
accz_offset=-462.44
gyrox_offset=346.405
gyroy_offset=49.6775
gyroz_offset=19.725
accel_scale=8192
gyro_scale=65.5

def stream(data):
  global df
  global accx_offset, accy_offset, accz_offset
  global gyrox_offset, gyroy_offset, gyroz_offset
  global accel_scale, gyro_scale
  global acc_roll, acc_pitch
  global gyro_roll, gyro_pitch, gyro_yaw

  accx=(data.linear_acceleration.x+accx_offset)/accel_scale * gravity_standart
  accy=(data.linear_acceleration.y+accy_offset)/accel_scale * gravity_standart
  accz=(data.linear_acceleration.z+accz_offset)/accel_scale * gravity_standart
  gyrox=(data.angular_velocity.x+gyrox_offset)/gyro_scale * dps_to_rps
  gyroy=(data.angular_velocity.y+gyroy_offset)/gyro_scale * dps_to_rps
  gyroz=(data.angular_velocity.z+gyroz_offset)/gyro_scale * dps_to_rps

  imu_msg=Imu()
  imu_msg.header.frame_id = IMU_FRAME	
  imu_pub=rospy.Publisher('imu/data', Imu, queue_size=10)
  
  imu_msg.linear_acceleration.x=accx
  imu_msg.linear_acceleration.y=accy
  imu_msg.linear_acceleration.z=accz
    
  imu_msg.angular_velocity.x=gyrox
  imu_msg.angular_velocity.y=gyroy
  imu_msg.angular_velocity.z=gyroz

  
  imu_pub.publish(imu_msg)
  imu_msg.header.stamp=rospy.Time.now()	
  print("Accelerations: ", accx, ", ",accy, ", ", accz, "  Gyros: ", gyrox, ", ", gyroy, ", ", gyroz)

  
  


def streamer():
  global df
  rospy.init_node('streamer', anonymous=True)
  IMU_FRAME=rospy.get_param('~imu_frame', 'imu_link')
  rospy.Subscriber("imu/data_raw", Imu, stream)
  rospy.spin()

if __name__ == '__main__':
   try:
    streamer()
   except rospy.ROSInterruptException:
    pass