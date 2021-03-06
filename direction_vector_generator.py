import cv2

"""
Finds the longest vector without obstruction from the bottom center 
of an image.
"""
import numpy as np
import scipy

class DirectionVectorGenerator:
    def __init__(self , resolution=11, image_size=(640,480)):
        self._resolution = resolution
        self._image_width = image_size[0]
        self._image_height = image_size[1]
        self._origin = (int(self._image_width/2),self._image_height)
        self._max_obstacle_distance = 80
        self._obstacle_field_of_view = np.pi/12
        self._distance_scale = 4
        self._masks = []
        self._angles = []
        self.generate_masks_and_angles()

    def generate_masks_and_angles(self):
        # Generate masks and their angles
        xs = np.linspace(0,self._image_width,self._resolution)
        blank = np.zeros((self._image_height, self._image_width), np.uint8)
        for x in xs:
            endpoint = (int(x), 0)
            mask = np.copy(blank)
            cv2.line(mask, self._origin, endpoint, 255, 2)
            # cv2.imshow("mask", mask)
            # cv2.waitKey(0)
            self._masks.append(mask)
            if x != self._image_width/2:
                angle = np.arctan((x-self._image_width/2)/self._image_height)
            else:
                angle = 0
            self._angles.append(angle)
        self._angles = np.array(self._angles)

    def check_intersections(self,mask,img):
        # Check for intersects with each ray
        img[0,:] = 255
        # img = cv2.resize(img, (self._image_width, self._image_width))
        intersects = cv2.bitwise_and(mask, img)
        # cv2.imshow('intersections',intersects)
        # cv2.waitKey(1)
        return intersects
    
    def get_direction_vector_average(self,image):
        number_of_angles = len(self._angles)
        stream_lengths = np.zeros(number_of_angles)
        for i in range(number_of_angles):
            mask = self._masks[i]
            intersections = self.check_intersections(mask,image)
            intersection_locations = np.vstack(np.where(intersections > 0))
            difference = np.flip(intersection_locations,axis=0).T - np.asarray(self._origin)
            intersection_distances = np.linalg.norm(difference,2,1)
            scale = 4
            stream_lengths[i] = np.clip(intersection_distances.min(), 0, (self._image_height*8/9))
        weights = stream_lengths**scale
        avg_stream_angle = np.average(self._angles, weights=weights)
        is_too_close = self.check_if_obstacles_are_too_close(stream_lengths)
        index_chosen_angle = np.argmin(np.abs(self._angles - avg_stream_angle))
        return stream_lengths[index_chosen_angle], avg_stream_angle, self._masks[index_chosen_angle], is_too_close
        # return max_stream_length, stream_angle, mask
        
    def get_direction_vector(self,image):
        number_of_angles = len(self._angles)
        stream_lengths = np.zeros(number_of_angles)
        for i in range(number_of_angles):
            mask = self._masks[i]
            intersections = self.check_intersections(mask,image)
            intersection_locations = np.vstack(np.where(intersections > 0))
            difference = np.flip(intersection_locations,axis=0).T - np.asarray(self._origin)
            intersection_distances = np.linalg.norm(difference,2,1)
            closest_point = intersection_locations[:,np.argmin(intersection_distances)]
            stream_lengths[i] = np.clip(intersection_distances.min(), 0, self._image_height*8/9)
        max_stream_length = np.max(stream_lengths)
        index_max_stream = np.argmax(stream_lengths)
         
        # Check for duplicates, choose the smallest angle among them
        unique,counts = np.unique(stream_lengths, return_counts=True)

        duplicates = unique[counts>1]
        
        # Only care about duplicates of the max length
        if (duplicates == max_stream_length).any():
            idx = stream_lengths == max(duplicates)
            duplicate_angles = self._angles[idx]
            index_max_stream = np.argmin(abs(duplicate_angles))
            stream_angle = duplicate_angles[index_max_stream]
            mask = self._masks[np.where(self._angles==stream_angle)[0][0]]
        else:           
            stream_angle = self._angles[index_max_stream]
            mask = self._masks[index_max_stream]
        
        
        weights = np.clip(stream_lengths, 0, self._image_height/2)
        avg = np.average(self._angles, weights=weights)
        # print("avg:", np.degrees(avg))
        # print("angle", np.degrees(stream_angle))
        return max_stream_length, stream_angle, mask

    def check_if_obstacles_are_too_close(self, stream_lengths):
        streams_in_obstacle_fov = stream_lengths[np.abs(self._angles) < self._obstacle_field_of_view]
        streams_that_are_too_short = streams_in_obstacle_fov[streams_in_obstacle_fov < self._max_obstacle_distance]
        number_of_short_streams_tolerance = np.ceil(len(streams_in_obstacle_fov)/2)
        if len(streams_that_are_too_short) >= number_of_short_streams_tolerance:
            return True
        else:
            return False
        

