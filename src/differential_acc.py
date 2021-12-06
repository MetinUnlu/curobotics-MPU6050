#!/usr/bin/env python

import rospy
import math
from sensor_msgs.msg import Imu
import pandas as pd
from time import time
from datetime import datetime
from math import sin, cos, tan, pi
import numpy as np

accx=accy=accz=0.0

accx_list=[]
accy_list=[]
accz_list=[]

accx_std=0.01283*1.5
accy_std=0.01284*1.5
accz_std=0.017649693*1.5

velx=0.0

dispx=0.0

i=0

dt=0.0
start_time=time()

def deviation_control(value, deviation):
	if value > deviation or value < -deviation:
		pass
	else:
		value=0
	return value


def stream(data):
	global accx,accy,accz
	global velx, dispx
	global dt, start_time
	global i

	dt = time()- start_time
	start_time=time()
	
	accx_dif=data.linear_acceleration.x-accx
	accy_dif=data.linear_acceleration.y-accy
	accz_dif=data.linear_acceleration.z-accz

	accx=data.linear_acceleration.x
	accy=data.linear_acceleration.y
	accz=data.linear_acceleration.z

	
	

	accx_dif=deviation_control(accx_dif,accx_std)
	accy_dif=deviation_control(accy_dif,accy_std)
	accz_dif=deviation_control(accz_dif,accz_std)

	dispx=dispx+velx*dt+accx_dif*dt**2/2
	velx=velx+accx_dif*dt

	print("%.2f"%accx_dif,"%.2f"%accy_dif,"%.2f"%accz_dif)
	print("Displacement: ", "%.2f"%dispx,"Velocity: ","%.2f"%velx)
	'''
	accx_list.append(accx_dif)
	accy_list.append(accy_dif)
	accz_list.append(accz_dif)

	
	if i < 1000:
		i =i+1
	else:
		accx_list.pop(0)
		accy_list.pop(0)
		accz_list.pop(0)
		print("Accx is: ", np.std(accx_list), " & Accy is: ", np.std(accy_list), " & Accy is: ", np.std(accz_list))
	'''
  


def streamer():
	global df
	IMU_FRAME=rospy.get_param('~imu_frame', 'imu_link')
	rospy.Subscriber("imu/data", Imu, stream)
	rospy.spin()

if __name__ == '__main__':
	rospy.init_node('streamer', anonymous=True) 
	try:
		streamer()
	except rospy.ROSInterruptException:
		pass