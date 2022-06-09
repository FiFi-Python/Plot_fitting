#import packages
import sys
import math
import cv2
import cv2 as cv
import numpy as np

def rotate_bound(image, angle, line1, line2):

    (h, w) = image.shape[:2]
    cX=round((line1[0]+line1[2]+line2[0]+line2[2])/4)
    cY=round((line1[1]+line1[3]+line2[1]+line2[3])/4)

    M = cv2.getRotationMatrix2D((round(cX), round(cY)), -angle, 1.0)#rotation matrix around point, angle,

    cos = np.abs(M[0, 0])
    sin = np.abs(M[0, 1])

        # compute the new bounding dimensions of the image
    nW = int((h * sin) + (w * cos))
    nH = int((h * cos) + (w * sin))

        # adjust the rotation matrix to take into account translation
    M[0, 2] += (nW / 2) - cX
    M[1, 2] += (nH / 2) - cY
        # perform the actual rotation and return the image

    return cv2.warpAffine(image, M, (nW, nH))
