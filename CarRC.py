# $ python3 CarTest.py

'''
******* Controlling The Car **********
    By DJ Lee on February 5, 2022

    Use $ ls /dev/tty* to list all ports connected to the computer and enter it below to establish serial communication.
    Turn off the power on the USB hub that is connected to the Arduino board.
    Press the ESC power button for one second and make sure the LED turns solid red.
    There are seven commands you can use to communicate with the car
        steer: steers the car from -30 to 30 degrees, e.g., steer15 to turn right 15 degrees.
        drive: sets speed to drive from -3.0 to 3.0 meters per second, e.g., drive1.2 to drive at 1.2 m/s.
        zero: sets the pwm value for the car to go straight (0 degree) usually very close to 1500.
            Use this command to try different PWM values and send steer0 comand to see if it goes straight.
            This command with the correct PWM for your vehicle must be called when starting your program.
        encoder: reads and returns the encoder count.
        pid: selects to enable (1) or disable PID control, e.g., pid1 to turn on PID.
        KP: sets proportion (between 0 and 1) for PID, e.g., KP0.2 to set KP to 0.2.
        KD: sets differential (between 0 and 1) for PID, e.g., KD0.02 to set KD to 0.02.
	EXTREMELY IMPORTANT: Be very careful whe controlling the car.
	NEVER tell it to go full speed. Safely test the car to find a safe range for your particular car
	and don't go beyond that speed. These cars can go very fast, and there is expensive hardware
	on them, so don't risk losing control of the car and breaking anything.
**************************************
'''

from Arduino import Arduino
import time
# import pygame
# from pygame.locals import *
from pynput.keyboard import Key, Listener
# import Keyboard

keys = [False, False, False, False]
Car = Arduino("/dev/ttyUSB0", 115200) 

def on_press(key):
    # print('{0} pressed'.format(
    #     key))
    if key==Key.up and not keys[2]:
        Car.drive(2.5)
        keys[0]=True
    elif key==Key.left and not keys[3]:
        Car.steer(-30)
        keys[1]=True
    elif key==Key.down and not keys[0]:
        Car.drive(-2.5)
        keys[2]=True
    elif key==Key.right and not keys[1]:
        Car.steer(30)
        keys[3]=True

def on_release(key):
    # print('{0} release'.format(
    #     key))
    if key == Key.esc:
        # Stop listener
        return False
    if key==Key.up:
        Car.drive(0)
        keys[0]=False
    elif key==Key.left:
        Car.steer(0)
        keys[1]=False
    elif key==Key.down:
        Car.drive(0)    
        keys[2]=False
    elif key==Key.right:
        Car.steer(0)
        keys[3]=False

# keyboard.on_press(on_press)
# keyboard.on_release(on_release)

# while True:
#     time.sleep(1)
# while True:
with Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()

