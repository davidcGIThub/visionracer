import numpy as np

class DrivingLogic:
    def __init__(self):
        self._state = 'STOP'

    def drive(self):
        if self._state == 'STOP':
            self.stop_actions()
        elif self._state == 'RACE':
            self.race_actions()
        elif self._state == 'BACK_UP':
            self.back_up_actions

    def stop_actions(self):
        if self.check_if_car_is_in_race_mode():
            if self.check_if_obstacles_are_too_close():
                self._state = 'RACE'
            else:
                self._state = 'BACK_UP'

    def race_actions(self):
        if self.check_if_car_is_in_race_mode():

    def back_up_actions(self):
        #TODO
        pass

    def check_if_car_is_stuck(self):
        #TODO
        pass

    def check_if_obstacles_are_too_close(self):
        #TODO
        pass

    def back_up_car(self):
        #TODO
        pass

    def drive_with_reactive_control(self):
        #TODO
        pass

    def check_if_car_is_in_race_mode(self):
        #TODO
        pass




