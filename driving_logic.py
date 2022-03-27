import numpy as np

class DrivingLogic:
    def __init__(self):
        self._state = 'STOP'
        self._TIME_TO_REVERSE = 50
        self._

    def drive(self):
        if self._state == 'STOP':
            self.stop_actions()
        elif self._state == 'RACE':
            self.race_actions()
        elif self._state == 'BACK_UP':
            self.back_up_actions

# STATES

    def stop_actions(self):
        if self.check_if_car_is_in_race_mode():
            if self.check_if_obstacles_are_too_close():
                self._state = 'BACK_UP'
            elif self.check_if_car_is_stuck():
                self._state = 'BACK_UP'
            else:
                self._state = 'RACE'
        else:
            #TODO 
            pass

    def race_actions(self):
        if self.check_if_car_is_in_race_mode():
            if self.check_if_obstacles_are_too_close():
                self._state = 'BACK_UP'
            elif self.check_if_car_is_stuck():
                self._state = 'BACK_UP'
            else:
                self.drive_with_reactive_control()
        else:
            self._state = 'STOP'

    def back_up_actions(self):
        if self.check_if_car_is_in_race_mode():
            if self.check_if_backed_up_long_enough():
                if self.check_if_obstacles_are_too_close():
                    #TODO
                    pass
                else:
                    self._state = 'RACE'
            else:
                self.back_up_car()
        else:
            self._state = 'STOP'

# FUNCTIONS

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

    def check_if_backed_up_long_enough(self):
        #TODO
        pass




