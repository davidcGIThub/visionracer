import cv2
import numpy as np
# from direction_vector_generator import DirectionVectorGenerator
from direction_vector_generator_extended import DirectionVectorGenerator
from reactive_controller import ReactiveController
from birdseye import birdsEye
import time

file = "Video.avi"
video = cv2.VideoCapture(file)
processor = birdsEye(file = "transform2.npz")

intersects = DirectionVectorGenerator(21, (640, processor.height))
controller = ReactiveController(velocity_gain=2.5/640, angle_gain=30/46)
img_file = "pictures/"
while(video.isOpened()):
    ret, img = video.read()
    if ret:
        cv2.imshow("test", img)
        processor.process(img)
        processor.homography()
        max_stream_length, stream_angle, mask, is_too_close = intersects.get_direction_vector_average(processor.combined)
        mask = cv2.resize(mask, (640,316))
        cv2.imshow("obstacles", processor.combined+mask)
        # Control
        velocity_command, angle_command = controller.proportional_control(max_stream_length, stream_angle)
        # command_mask = processor.combined+mask
        # cv2.line(command_mask, intersects._origin,(240*np.cos()))
        # cv2.imshow("command")
        print(velocity_command, angle_command)

        k= cv2.waitKey(1)
        if k == ord("q"):
            break

    else:
        cv2.destroyAllWindows()
        break