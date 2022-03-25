import cv2
import numpy as np
        

# Mask creator

def mask(angle, width = 640, height = 316):
    blank = np.zeros((height, width), np.uint8)
    origin = (int(width/2),height)
    endx = origin[0] + height * np.tan(np.radians(angle))
    endpoint = (int(endx), 0)
    cv2.line(blank, origin, endpoint, 255, 2)
    return blank


if __name__ == "__main__":       
    width = 640 
    height = 480

    blank = np.zeros((height, width))

    cv2.imshow("blank", blank)
    cv2.waitKey()

    origin = (int(width/2),height)

    xs = np.linspace(0,width,11)

    masks = []
    angles = []
    for x in xs:
        endpoint = (int(x), 0)
        mask = np.copy(blank)
        cv2.line(mask, origin, endpoint, 255, 1)
        cv2.imshow("mask", mask)
        cv2.waitKey(0)
        masks.append(mask)
        if x != width/2:
            angle = np.arctan((x-width/2)/height)
        else:
            angle = 0
        angles.append(angle)
