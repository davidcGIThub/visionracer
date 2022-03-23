"""
Finds the longest vector without obstruction from the bottom center 
of an image.
"""
import numpy as np
from scipy.optimize import fsolve

class DirectionVectorGenerator:
    def __init__(self , resolution,
                        image_size):
        