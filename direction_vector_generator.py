import cv2

"""
Finds the longest vector without obstruction from the bottom center 
of an image.
"""
import numpy as np
from scipy.optimize import fsolve

class DirectionVectorGenerator:
    def __init__(self , resolution=11, image_size=(640,480)):
        self._resolution = resolution
        self._image_width = image_size[0]
        self._image_height = image_size[1]
        self._origin = (int(self._image_width/2),self._image_height)
        self._masks = []
        self._angles = []
        self.generate_masks_and_angles()

    def generate_masks_and_angles(self):
        # Generate masks and their angles
        xs = np.linspace(0,self._image_width,self._resolution)
        blank = np.zeros((self._image_height, self._image_width))
        for x in xs:
            endpoint = (int(x), 0)
            mask = np.copy(blank)
            cv2.line(mask, self._origin, endpoint, 255, 1)
            cv2.imshow("mask", mask)
            cv2.waitKey(0)
            self._masks.append(mask)
            if x != self._image_width/2:
                angle = np.arctan((x-self._image_width/2)/self._image_height)
            else:
                angle = 0
            self._angles.append(angle)
        