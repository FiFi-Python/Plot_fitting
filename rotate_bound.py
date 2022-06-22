# import packages
import sys
import math
import cv2
import cv2 as cv
import numpy as np


###############

def rotate_bound(image, line1, line2):
    def Rotation_matrix_and_bounds(image, cX, cY, phi):
        M = cv2.getRotationMatrix2D((cX, cY), phi, 1.0)
        cos = np.abs(M[0, 0])
        sin = np.abs(M[0, 1])

        # compute the new bounding dimensions of the image

        nW = round(1.6 * w)  # int((h * sin) + (w * cos))
        nH = round(1.6 * h)  # int((h * cos) + (w * sin))

        # adjust the rotation matrix to take into account translation
        M[0, 2] += (nW / 2) - cX
        M[1, 2] += (nH / 2) - cY
        points = np.array([[cX, cY]])

        #  transfrom center
        ones = np.ones(shape=(len(points), 1))
        points_ones = np.hstack([points, ones])
        transformed_points = M.dot(points_ones.T).T
      #  cv.imshow("obrot0",cv2.warpAffine(image, M, (nW, nH)),(round(transformed_points[0][0]))
      #  cv.waitKey()

        return [cv2.warpAffine(image, M, (nW, nH)),(round(transformed_points[0][0]),round(transformed_points[0][1]))]#0

    delx1 = line1[2] - line1[0]
    delx2 = line2[2] - line2[0]
    dely1 = line1[3] - line1[1]
    dely2 = line2[3] - line2[1]

    y10 = line1[1]
    y20 = line2[1]

    (h, w) = image.shape[:2]

    if (delx1 != 0 and delx2 != 0):  # no vertical lines

        a1 = dely1 / delx1
        a2 = dely2 / delx2
        b1 = line1[1] - line1[0] * a1
        b2 = line2[1] - line2[0] * a2

        cX = (b2 - b1) / (a1 - a2)
        cY = a1 * cX + b1

       # prime = cv.circle(image, (round(cX), round(cY)), 50, (255, 0, 0), -1)

        tg_phi = dely2 / delx2
        phi = math.atan(tg_phi) * 180 / math.pi

        return [Rotation_matrix_and_bounds(image, cX, cY, phi + x * 90) for x in
                range(0, 4)]  # cv2.warpAffine(image, M, (nW, nH))
    else:
        phi = 0
        if (abs(delx2) < abs(delx1)):  # second line is vertical
            cX = round((line2[0] + line2[2]) / 2)  # point of rotation
            cY = round(dely1 / delx1 * cX + line1[1])
            return [Rotation_matrix_and_bounds(image, cX, cY, phi + x * 90) for x in
                    range(0, 4)]  # cv2.warpAffine(image, M, (nW, nH))

        else:  # druga prosta jest pionowa
            cX = round((line1[0] + line1[2]) / 2)  # point of rotation
            cY = round(dely2 / delx2 * cX + line2[1])

            return [Rotation_matrix_and_bounds(image, cX, cY, phi + x * 90) for x in range(0, 4)]

