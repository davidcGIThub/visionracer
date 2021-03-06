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
import cv2
from birdseye import birdsEye
from direction_vector_generator import DirectionVectorGenerator
# from direction_vector_generator_extended import DirectionVectorGenerator
from reactive_controller import ReactiveController
import time
from maskgen import mask as m

# Instantiate lane detection, angle detector and controller
detector = birdsEye(img_height=480)
generator = DirectionVectorGenerator(31, (640,detector.height))
controller = ReactiveController(velocity_gain=1.5/316, angle_gain=30/66)

rs = RealSense("/dev/video2", RS_VGA)		# RS_VGA, RS_720P, or RS_1080P
video_out = cv2.VideoWriter('hw8_video.avi',cv2.VideoWriter_fourcc(*'XVID'),30,(640,480))
record = True
# Use $ ls /dev/tty* to find the serial port connected to Arduino
Car = Arduino("/dev/ttyUSB0", 115200)                # Linux
#Car = Arduino("/dev/tty.usbserial-2140", 115200)    # Mac

Car.zero(1500)      # Set car to go straight.  Change this for your car.
Car.pid(1)          # Use PID control
# You can use kd and kp commands to change KP and KD values.  Default values are good.
# loop over frames from Realsense
# prev_encoder_reading = Car.encoder()
num_encoder_same = 0

# Wait for user input to continue
wait = input("\nVisionracer Initialized\n\n Press ENTER to start your race!")

num_low_norm = 0
first = True
start_time = time.time()
while True:
    (t, rgb, depth, accel, gyro) = rs.getData()
    if record:
        video_out.write(rgb)
    
    # Detect obstacles
    detector.process(rgb)
    toc1 = time.time()
    print("here")
    # Generate an optimal path
    length, angle, mask, is_too_close = generator.get_direction_vector_average(detector.combined)
    # angle = np.degrees(angle)
    mask = cv2.resize(mask, (640,316))
    
    # Compute control 
    velocity_command, angle_command = controller.proportional_control(length, angle) 
    angle_show = m(np.degrees(angle))
    # cv2.imshow("obstacles", detector.combined+angle_show)
    
    
    print("ACCELL: ", np.linalg.norm(accel))
    print("GYROOO: ", np.linalg.norm(gyro))
    if np.linalg.norm(accel) <= 9.8 and np.linalg.norm(gyro) < .02:
        num_low_norm += 1
    else:
        num_low_norm = 0

    if num_low_norm > 2 and not first and time.time() - start_time > 2:
        num_low_norm = 0
        velocity_command = controller.back_up_command()
        Car.drive(velocity_command)
        Car.steer(0)
        time.sleep(1.5)

    # if is_too_close and not first and time.time() - start_time > 2:
    #     num_low_norm = 0
    #     velocity_command = controller.back_up_command()
    #     Car.drive(velocity_command)
    #     Car.steer(0)
    #     time.sleep(1.5)


    
    
    Car.steer(angle_command)
    Car.drive(velocity_command)

    first = False
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
    # key = cv2.waitKey(1) & 0xFF
    # if key == ord("q"):
    #     break
del rs
del Car

