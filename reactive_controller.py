"""
Reactive controller for rc car with stereo vision
"""
import numpy as np
from scipy.optimize import fsolve

class ReactiveController:
    def __init__(self,  body_length = 0.2032, # (m) wheel to wheel length of car
                        back_wheel_to_camera_length = 
                        max_velocity = 3, # (m/s) max velocity of car 
                        max_wheel_angle = np.pi/6, # (rad) max turn angle of wheels
                        velocity_gain = 1, # gain coeficient for velocity
                        angle_gain = 1
                        ):
        self._L = body_length
        self._v_max = max_velocity
        self._delta_max = max_wheel_angle
        self._kp_v = velocity_gain
        self._kp_theta = angle_gain

    def proportional_control(self, stream_length, desired_direction, current_wheel_angle):
        velocity_commmand = np.min(self._v_max, self._kp_v * stream_length)
        center_length = self._L/2
        # def wheel_angle_function(delta):
        #     center_length = self._L/2
        #     beta = np.arctan2(center_length * np.tan(delta) , self._L)
        #     f = velocity_commmand*np.cos(beta)*np.tan(delta)/self._L - self._kp_theta*desired_direction
        #     return f
        wheel_angle_command = np.clip(np.arctan2(self._L*desired_direction/center_length)  ,-self._delta_max,self._delta_max)
        return velocity_commmand, wheel_angle_command
