"""
Demo moving the end link back and forth sinusoidally
"""
import time

import numpy as np

import ui
from robot import Robot
# Uncomment the following for simulation
#from robot import SimulatedRobot as Robot

with Robot.connect() as r, ui.basic(r) as gui:
    while gui.open:
        t = time.time()
        f = 0.5  # Hz
        A = np.radians(45)
        r.servo_angle = np.array([-A*0.5, 0, A])*np.sin(2*np.pi*f*t)
        time.sleep(0.01)
