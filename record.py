from RealSense import *

rs = RealSense("/dev/video2", RS_1080P)
video_out = cv2.VideoWriter('scene.avi',cv2.VideoWriter_fourcc(*'XVID'),30,(1920,1080))

while(True):
    (time, rgb, depth, accel, gyro) = rs.getData()
    video_out.write(rgb)