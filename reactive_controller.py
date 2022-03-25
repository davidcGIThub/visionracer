"""
Reactive controller for rc car with stereo vision
"""
import numpy as np
from scipy.optimize import fsolve

class ReactiveController:
    def __init__(self,  body_length = 0.2032, # (m) wheel to wheel length of car
                        back_wheel_to_camera_length = 0.1143, # (m) back wheel to camera length
                        max_velocity = 3, # (m/s) max velocity of car 
                        max_wheel_angle = np.pi/6, # (rad) max turn angle of wheels
                        velocity_gain = 1, # gain coeficient for velocity
                        angle_gain = 1
                        ):
        self._L = body_length
        self._lr = back_wheel_to_camera_length
        self._v_max = max_velocity
        self._delta_max = max_wheel_angle
        self._kp_v = velocity_gain
        self._kp_theta = angle_gain

    def proportional_control(self, stream_length, desired_direction):
        velocity_commmand = np.min((self._v_max, self._kp_v * stream_length))
        # wheel_angle_command = np.clip(np.arctan2(self._L*desired_direction, self._lr)  ,-self._delta_max,self._delta_max)
        # wheel_angle_command = desired_direction * self._kp_theta
        wheel_angle_command = desired_direction**3 * 0.000308 
        return velocity_commmand, np.degrees(wheel_angle_command)
