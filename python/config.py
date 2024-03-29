import numpy as np

N = 3

# the pulses corresponding to 0 and 90 degrees
servo_0_90 = np.array([
	[1170, 2040],
	[1410, 2274],
	[1217, 2055]
])
servo_per_radian = (servo_0_90[:,1] - servo_0_90[:,0]) / np.radians(90)
servo_0 = servo_0_90[:,0]

# the limits beyond which the servo can't tell the difference, and might cause
# damage
servo_limits = (550, 2300)
servo_angle_limits = (np.array(servo_limits) - servo_0[:,np.newaxis]) / servo_per_radian[:,np.newaxis]

# the length of the links, in meters
lengths = np.array([
	0.125,
	0.148,
	0.149,
	0.139
])

# These are the adc readings when a link is held horizontally, and the adjacent
# link allowed to fall under gravity. The heavier side of the joint is the on
# that should be held. By repeating the experiment with the setup upsidedown,
# we should get two torques that sum to zero, giving us the reading
# corresponding to zero torque
_adc_zero = np.array([
	[515, 525],
	[455, 600],
	[519, 544]
])
adc_0 = _adc_zero.mean(axis=1)

#See Link 3 Data.txt for 
adc_0[2] = 528.7845903
rad_per_adc = np.radians(0.368583536)

# the limits which cannot be actively driven beyond
adc_active_lims = np.array([
	(425, 590),
	(422, 619),
	(460, 616)
])
adc_passive_lims = np.array([(360, 680)] * 3)
error_active_lim = (adc_active_lims - adc_0[:,np.newaxis]) * rad_per_adc

# TODO: https://github.com/eric-wieser/4m20-coursework2/issues/12
com = lengths / 2

# TODO: https://github.com/eric-wieser/4m20-coursework2/issues/4
_total_mass = 0.40
masses = _total_mass * np.ones(4) / 4

max_torque = 0.250 * lengths[0] * 9.81

# Make everything read only!
for key, val in list(locals().items()):
	if isinstance(val, np.ndarray):
		val.setflags(write=False)

if __name__ == '__main__':
	print('Config')
	print('------')
	print('servo_0:', servo_0)
	print('servo_per_radian:', servo_per_radian)
	print('servo_angle_limits:', servo_angle_limits)
	print('adc_0:', adc_0)
	print('rad_per_adc:', rad_per_adc)
	print('adc_active_lims:', adc_active_lims)
	print('error_active_lim:', error_active_lim)
	print('lengths:', lengths)
	print('masses:', masses)
	print('max_torque:', max_torque)