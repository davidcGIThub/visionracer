import cv2
import numpy as np
from direction_vector_generator import DirectionVectorGenerator
from reactive_controller import ReactiveController

class birdsEye:
    def __init__(self, file=None, img_height=480) -> None:
        if file is not None:
            self.transform = np.load(file)['arr_0'] # File containing birdseye view transformation
        self.kernel = np.ones((3,3), np.uint8)
        self.rect = []
        self.pointsCollected = False
        
        self.top_crop = int(0.3 * img_height)
        self.bottom_crop = int(0.96 * img_height)
        self.height = self.bottom_crop - self.top_crop

    def process(self, img):
        self.colorSegment(img)
        self.lane_lines()
        # self.homography()
        
        # cv2.waitKey(1)
        

    def colorSegment(self, img):
        img = img[self.top_crop:self.bottom_crop,:,:]

        # Split into bgr and hsv
        # cv2.imshow("test", img)
        self.bgr = img
        self.hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        b,g,r = cv2.split(self.bgr)
        h,s,v = cv2.split(self.hsv)
        
        # Threshold on s and b
        _, threshS = cv2.threshold(s, 80, 255, cv2.THRESH_BINARY)
        _, threshB = cv2.threshold(b, 130, 255, cv2.THRESH_BINARY)
        _, threshG = cv2.threshold(g, 135, 255, cv2.THRESH_BINARY)
        _, threshR = cv2.threshold(r, 190, 255, cv2.THRESH_BINARY)

        # Remove noise
        # morphS = cv2.morphologyEx(threshS, cv2.MORPH_OPEN, self.kernel)
        # morphG = cv2.morphologyEx(threshG, cv2.MORPH_OPEN, self.kernel)
        # cv2.imshow("morph_s", morphG)
        # cv2.imshow("morph_b", morphB)

        self.lanes = cv2.bitwise_and(threshG, threshS)
        self.cones = cv2.bitwise_and(threshR, threshS)
        self.lanes = cv2.morphologyEx(self.lanes, cv2.MORPH_OPEN, self.kernel)
        self.cones = cv2.morphologyEx(self.cones, cv2.MORPH_OPEN, self.kernel)


    def lane_lines(self):
        lines = cv2.HoughLinesP(self.lanes, 1, np.pi/180, 30, maxLineGap=60)
        self.lanes_filled = np.copy(self.lanes)
        # draw Hough lines
        if lines is not None:
            for line in lines:
                x1, y1, x2, y2 = line[0]
                cv2.line(self.lanes_filled, (x1, y1), (x2, y2), 255, 3)
        
        self.combined = self.lanes_filled + self.cones

    def homography(self):
        # Apply transformation to generate birdseye view
        IMAGE_H, IMAGE_W = self.lanes.shape
        warped_img = cv2.warpPerspective(self.lanes_filled, self.transform, (IMAGE_W, IMAGE_H))
        # cv2.imshow("birdseye", warped_img)

    def homographyCalib(self):
        # Solve for the transform that generates a birdseye view

        # Callback for choosing points
        cv2.setMouseCallback("test", self.callback)
        print("select 4 points on a 5x8 pattern")
        while not self.pointsCollected:
            cv2.waitKey(1)
        
        # Apply homography for birdseye view
        IMAGE_H, IMAGE_W = self.lanes.shape
        src = np.float32(self.rect)
        base = 200
        height = base*5/8
        down = (IMAGE_H-height)/2
        over = (IMAGE_W - base)/2
        # dst = np.float32([self.rect[0], self.rect[1], [self.rect[0][0], self.rect[2][1]], [self.rect[1][0], self.rect[3][1]]])
        dst = np.float32([[over,down], [over+base,down], [over,down+height], [over+base,down+height]])
        # src = np.float32([[0, IMAGE_H], [IMAGE_W, IMAGE_H], [0, 0], [IMAGE_W, 0]])
        # dst = np.float32([[320, IMAGE_H], [423, IMAGE_H], [0, 0], [IMAGE_W, 0]])
        M = cv2.getPerspectiveTransform(src, dst) # The transformation matrix
        Minv = cv2.getPerspectiveTransform(dst, src) # Inverse transformation
        # combined = self.cones + self.lanes
        warped_img = cv2.warpPerspective(img, M, (IMAGE_W, IMAGE_H)) # Image warping
        cv2.imshow("birdseye", warped_img)
        np.savez("./visionracer/transform2.npz", M)
        

    def callback(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            self.rect.append([x,y])
            print(x,y)
            if len(self.rect) == 4:
                self.pointsCollected = True



if __name__ == "__main__":
    # Testing
    import os
    print(os.getcwd())
    processor = birdsEye(file = "./visionracer/transform2.npz")
    # img = cv2.imread("./pictures/img3.png")
    # cv2.imshow("test", img)
    # processor.process(img)
    intersects = DirectionVectorGenerator(21, (640, processor.height))
    controller = ReactiveController(velocity_gain=2.5/640, angle_gain=1)
    img_file = "./pictures/"
    for file in os.listdir(img_file):
        img = cv2.imread(img_file+file)
        cv2.imshow("test", img)
        processor.process(img)
        max_stream_length, stream_angle, mask = intersects.get_direction_vector(processor.lanes+processor.cones)
        mask = cv2.resize(mask, (640,316))
        cv2.imshow("obstacles", processor.combined+mask)
        k= cv2.waitKey(1)
        if k == ord("q"):
            break

        # Control
        velocity_command, angle_command = controller.proportional_control(max_stream_length, stream_angle) 
        print(velocity_command, angle_command)
    