"""
4D State Space Kalman Filter

Requires:
	- Python 3
"""

from math import *
#Note: this code uses a custom matrix class from Udacity site.  

def show(value):
	for i in range(len(value)):
		print(value[i])

def filter(x, P):
	for n in range(len(measurements)):

		#prediction
		x = (F * x) + u
		P = F * P * F.transpose()

		#measurement update
		Z = matrix([measurements[n]])
		y = Z.transpose() - (H * x)
		S = H * P * H.transpose()
		K = P * H.transpose() + R
		x = x + (K * y)
		P = (I - (K * H)) * P

	print('x=')
	x.show()
	print('P=')
	P.show()
		
measurements = [[5., 10.], [6., 8.], [7., 6.], [8., 4.], [9., 2.], [10., 0.]]
initial_xy = [4., 12.]

dt = 0.1

#initial state (location and velocity)
x = matrix([[initial_xy[0]], [initial_xy[1]], [0.], [0.]])

#external motion
u = matrix([[0.], [0.], [0.], [0.]])

#initial uncertainty: 0 for positions x and y, 1000 for the two velocities
P = matrix([[0., 0., 0., 0.], [0., 0., 0., 0.], [0., 0., 1000., 0.], [0., 0., 0., 1000.]])

#next state function: generalize the 2d version to 4d
F = matrix([[1., 0., dt, 0.], [0., 1., 0., dt], [0., 0., 1., 0.], [0., 0., 0., 1.]])

#measurement function: reflect the fact that we observe x and y but not the two velocities
H = matrix([[1., 0., 0., 0.], [0., 1., 0., 0.]])

#measurement uncertainty: use 2x2 matrix with 0.1 as main diagonal
R = matrix([[0.1, 0.], [0., 0.1]])

#4D identity matrix
I = matrix([[1., 0., 0., 0.], [0., 1., 0., 0.], [0., 0., 1., 0.], [0., 0., 0., 1.]])

filter(x, P)
