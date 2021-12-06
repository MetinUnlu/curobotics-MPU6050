#!/usr/bin/env python

import rospy
import math
from sensor_msgs.msg import Imu
import pandas as pd
from time import time
from datetime import datetime
from math import sin, cos, tan, pi
import numpy as np

df=pd.DataFrame(columns=["accx","accy","accz","gyrox","gyroy","gyroz"])

IMU_FRAME=None
dps_to_rps=0.017453293

C = np.array([[1, 0, 0, 0], [0, 0, 1, 0]])
P = np.eye(4)
Q = np.eye(4)
R = np.array([1.16*10**-6, 1.072*10**-6])

state_estimate = np.array([[0], [0], [0], [0]])

#Mean offset final calculation
#wk=state_estimate = np.array([[0.00327], [0], [0.00122], [0]])

#phi_acc_list=[]
#theta_acc_list=[]

#phi_hat_list=[]
#theta_hat_list=[]


dt=0.0

gyro_roll=0.0
gyro_pitch=0.0
gyro_yaw=0.0

acc_roll=0.0
acc_pitch=0.0
acc_yaw=0.0

phi_hat = 0.0
theta_hat = 0.0

start_time=time()

i=0

def stream(data):
	global dt, start_time, i
	global gyro_roll, gyro_pitch, gyro_yaw, acc_roll,acc_pitch,acc_yaw
	global state_estimate, C, P, Q, R, phi_hat, theta_hat
	global A,B, wk

	dt = time()- start_time
	start_time=time()

	accx=data.linear_acceleration.x
	accy=data.linear_acceleration.y
	accz=data.linear_acceleration.z

	phi_acc= math.atan2(accy, math.sqrt(accx ** 2.0 + accz ** 2.0))
	theta_acc = math.atan2(-accx, math.sqrt(accy ** 2.0 + accz ** 2.0))

	"""
	phi_acc_list.append(phi_acc)
	theta_acc_list.append(theta_acc)
	
	if i < 1000:
		i =i+1
	else:
		phi_acc_list.pop(0)
		theta_acc_list.pop(0)
		#print("Phi variance is: ", np.var(phi_acc_list), "with ", phi_acc, " & Theta variance is: ", np.var(theta_acc_list), "with ", theta_acc)
	"""



	gyrox=data.angular_velocity.x
	gyroy=data.angular_velocity.y
	gyroz=data.angular_velocity.z

	phi_dot = gyrox + sin(phi_hat) * tan(theta_hat) * gyroy + cos(phi_hat) * tan(theta_hat) * gyroz
	theta_dot = cos(phi_hat) * gyrox - sin(phi_hat) * gyroz

	A = np.array([[1, -dt, 0, 0], [0, 1, 0, 0], [0, 0, 1, -dt], [0, 0, 0, 1]])
	B = np.array([[dt, 0], [0, 0], [0, dt], [0, 0]])

	gyro_input = np.array([[phi_dot], [theta_dot]])
	state_estimate = A.dot(state_estimate) + B.dot(gyro_input)
	P = A.dot(P.dot(np.transpose(A))) + Q

	measurement = np.array([[phi_acc], [theta_acc]])
	y_tilde = measurement - C.dot(state_estimate)
	S = R + C.dot(P.dot(np.transpose(C)))
	K = P.dot(np.transpose(C).dot(np.linalg.inv(S)))
	state_estimate = state_estimate + K.dot(y_tilde)
	P = (np.eye(4) - K.dot(C)).dot(P)

	phi_hat = state_estimate[0]
	theta_hat = state_estimate[2]

	"""
	phi_hat_list.append(phi_hat)
	theta_hat_list.append(theta_hat)

	
	if i < 1000:
		i =i+1
	else:
		phi_hat_list.pop(0)
		theta_hat_list.pop(0)
		print("Phi mean is: ", np.mean(phi_hat_list), " & Theta mean is: ", np.mean(theta_hat_list))
	print(state_estimate)
	"""

	# Display results
	print("Phi: " + str(round(phi_hat * 180.0 / pi, 1)) + " Theta: " + str(round(theta_hat * 180.0 / pi, 1)))







  
  


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