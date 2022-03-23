import cv2

"""
Finds the longest vector without obstruction from the bottom center 
of an image.
"""
import numpy as np
from scipy.optimize import fsolve

class DirectionVectorGenerator:
    def __init__(self , resolution,
                        image_size=(640,480)):


    width = image_size[0]
    height = image_size[1]
    origin = (int(width/2),height)

    # Generate masks and their angles
    xs = np.linspace(0,width,11)
    blank = np.zeros((height, width))
    self.masks = []
    self.angles = []
    for x in xs:
        endpoint = (int(x), 0)
        mask = np.copy(blank)
        cv2.line(mask, origin, endpoint, 255, 1)
        cv2.imshow("mask", mask)
        cv2.waitKey(0)
        self.masks.append(mask)
        if x != width/2:
            angle = np.arctan((x-width/2)/height)
        else:
            angle = 0
        self.angles.append(angle)
        