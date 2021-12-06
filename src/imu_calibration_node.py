#!/usr/bin/env python

import rospy
import math
from sensor_msgs.msg import Imu
import pandas as pd
from datetime import datetime

df=pd.DataFrame(columns=["accx","accy","accz","gyrox","gyroy","gyroz"])
gravity_value=9.80665

def stream(data):
  global df, gravity_value
  accx=data.linear_acceleration.x
  accy=data.linear_acceleration.y
  accz=data.linear_acceleration.z
  gyrox=data.angular_velocity.x
  gyroy=data.angular_velocity.y
  gyroz=data.angular_velocity.z
  
  df2={'accx':accx, 'accy': accy, 'accz': accz, 'gyrox': gyrox, 'gyroy': gyroy, 'gyroz': gyroz}
  ts=datetime.now().strftime("%H:%M:%S")
  new_row=pd.DataFrame([df2],index=[ts])
  df=pd.concat([df,pd.DataFrame(new_row)],ignore_index=False)

  if len(df.index)>400:
    df=df.iloc[1:,:]

  accx_offset=-df["accx"].mean()
  accy_offset=-df["accy"].mean()
  accz_offset=8192-df["accz"].mean()
  gyrox_offset=-df["gyrox"].mean()
  gyroy_offset=-df["gyroy"].mean()
  gyroz_offset=-df["gyroz"].mean()
  if len(df.index)==400:
    print('accx',accx_offset, 'accy', accy_offset, 'accz', accz_offset, 'gyrox', gyrox_offset, 'gyroy', gyroy_offset, 'gyroz', gyroz_offset)

  
  


def streamer():
  global df
  rospy.init_node('calibrator', anonymous=True)
  rospy.Subscriber("imu/data_raw", Imu, stream)
  rate=rospy.Rate(10)
  print(df)  
  while not rospy.is_shutdown():
    rate.sleep()

if __name__ == '__main__':
   try:
    streamer()
   except rospy.ROSInterruptException:
    pass