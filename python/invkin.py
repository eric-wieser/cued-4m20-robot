# angles defined in the same way as in the coursework,
# but all angles are clockwise in the positive direction

# phi1, phi2, phi3 are q1, q2 and q3

import numpy as np
from config import lengths
from config import servo_angle_limits as lims
from robot.base import State

def check_jacobian():
	"""
	Verify the jacobian computed in robot.base.State is correct, by comparing
	it with the symbolic jacobian of the positions.

	We can't check the positions, because we have nothing to check against.
	"""
	import sympy as sy
	# this is a hack to make np.cos(sympy thing) work properly
	sy.Basic.cos = lambda x: sy.cos(x)
	sy.Basic.sin = lambda x: sy.sin(x)

	# construct the angles and lengths as symbols
	angles = [sy.Symbol(r'\phi_{}'.format(i)) for i in [1, 2, 3]]
	lengths = np.array([sy.Symbol(r'l_{}'.format(i)) for i in [1, 2, 3, 4]])

	# make a state object with them
	s = State(joint_angles=angles).update(lengths=lengths)
	end_effector = s.joint_positions[-1]
	end_jacobian = s.joint_jacobians[-1][:,1:]

	# find the jacobian symbolically and otherwise
	expected = np.asarray(sy.Matrix(end_effector).jacobian(angles))
	actual = end_jacobian

	# compare them
	assert np.all(actual == expected)
	print("Jacobian is:")
	print(repr(actual))


# for this problem we want theta=0 to be the y axis, so just rotate things
rot90 = np.array([
	[0, -1],
	[1, 0]
])

def J(qq):
	# we want the jacobian of the last link, wrt all but the first link angle
	return rot90 @ State(joint_angles=qq).joint_jacobians[-1][:,1:]

def f(qq):
	return rot90 @ State(joint_angles=qq).joint_positions[-1]

def get_servo_angles(r, q=np.zeros(3), tol=0.001):
	# returns a set of servo values to send to the robot
	# the inputs are the coordinates for the desired location of the end effector
	r = np.asarray(r)
	# gradient descent until convergence
	while True:
		diff = r - f(q)
		if np.linalg.norm(diff) < tol:
			break

		jq = J(q)
		pjq = np.linalg.pinv(jq)

		# https://homes.cs.washington.edu/~todorov/courses/cseP590/06_JacobianMethods.pdf#page=13
		dq = pjq @ diff - (np.eye(jq.shape[1]) - pjq @ jq) @ q
		q = q + dq

	# normalize angles
	q = q % (2*np.pi)
	q[q > np.pi] -= 2*np.pi

	return q

def list_of_angles(listr, qstart): # list r needs to be a (2 x length) np array. 
	# qstart needs to be a np array with phi2, phi3 and phi4 in it (not including phi1 as it is assumed to be 0)
	l = listr.shape[0] # number of locations for the loop

	qreturn = np.zeros((l, 3))

	if listr.shape[1]!= 2:
		print('listr is in the wrong format - needs to be a 2 by (length) np array')
	if qstart.shape != (3,):
		print('qstart is in the wrong format - needs to be a np array with 3 elements in it')
	# start the algorithm off with qstart as the starting angles
	qreturn[0,:] = get_servo_angles(listr[0], qstart)

	for i in range(1,l): 	# make sure that it can get there
		qreturn[i,:] = get_servo_angles(listr[i], qreturn[(i-1),:]) # start off each run at the robot is currently
		if qreturn[i,0]<lims[0,0] or qreturn[i,0]>lims[0,1]:
			print('at index %d (python indexing starting at 0), q2 (%r) is out of range' % (i,qreturn[i,0]))
		if qreturn[i,1]<lims[1,0] or qreturn[i,1]>lims[1,1]:
			print('at index %d (python indexing starting at 0), q3 (%r) is out of range'% (i,qreturn[i,1]))
		if qreturn[i,2]<lims[2,0] or qreturn[i,2]>lims[2,1]:
			print('at index %d (python indexing starting at 0), q4 (%r) is out of range'% (i,qreturn[i,2]))
	return qreturn

if __name__ == '__main__':
	check_jacobian()

	q = get_servo_angles([0.3,0.3])
	np.testing.assert_allclose(f(q), [0.3, 0.3], atol=0.001, rtol=0)
