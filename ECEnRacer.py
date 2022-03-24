# python3 ECEnRacer.py
''' 
This program is for ECEN-631 BYU Race
*************** RealSense Package ***************
From the Realsense camera:
	RGB Data
	Depth Data
	Gyroscope Data
	Accelerometer Data
*************** Arduino Package ****************
	Steer(int degree) : -30 (left) to +30 (right) degrees
	Drive(float speed) : -3.0 to 3.0 meters/second
	Zero(int PWM) : Sets front wheels going straight around 1500
	Encoder() : Returns current encoder count.  Reset to zero when stop
	Pid(int flag) : 0 to disable PID control, 1 to enable PID control
	KP(float p) : Proporation control 0 ~ 1.0 : how fast to reach the desired speed.
	KD(float d) : How smoothly to reach the desired speed.

    EXTREMELY IMPORTANT: Read the user manual carefully before operate the car
**************************************
'''

# import the necessary packages
from Arduino import Arduino
from RealSense import *
import numpy as np
import imutils
import cv2
from birdseye import birdsEye
from direction_vector_generator import DirectionVectorGenerator
from reactive_controller import ReactiveController

# Instantiate lane detection, angle detector and controller
detector = birdsEye(img_height=1080)
generator = DirectionVectorGenerator(15, (1920,1080))
controller = ReactiveController(velocity_gain=2.5/1080)

rs = RealSense("/dev/video2", RS_1080P)		# RS_VGA, RS_720P, or RS_1080P
writer = None

# Use $ ls /dev/tty* to find the serial port connected to Arduino
Car = Arduino("/dev/ttyUSB0", 115200)                # Linux
#Car = Arduino("/dev/tty.usbserial-2140", 115200)    # Mac

Car.zero(1500)      # Set car to go straight.  Change this for your car.
Car.pid(1)          # Use PID control
# You can use kd and kp commands to change KP and KD values.  Default values are good.
# loop over frames from Realsense
while True:
    (time, rgb, depth, accel, gyro) = rs.getData()

    # Detect obstacles
    detector.process(rgb)

    # Generate an optimal path
    length, angle, mask = generator.get_direction_vector(detector.combined)
    mask = cv2.resize(mask, (1920,712))
    cv2.imshow("obstacles", detector.combined+mask)
    
    # Compute control 
    velocity_command, angle_command = controller.proportional_control(length, angle) 
    print(velocity_command, angle_command)
    '''
    Add your code to process rgb, depth, IMU data
    '''

    '''
    Control the Car
    '''

    '''
   	IMPORTANT: Never go full speed. Use CarTest.py to selest the best speed for you.
    Car can switch between positve and negative speed (go reverse) without any problem.
    '''
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break
del rs
del Car

