# import packages
import sys
import math
import cv2 as cv
import numpy as np
import argparse

# import functions
from rotate_bound import rotate_bound


def main(*argv):
    if (len(argv) > 0):
        filename = argv[0]
    else:
        print("Nie podano nazwy!")
        return -1

    # Loads an image
    original = cv.imread(cv.samples.findFile(filename))  # , cv.IMREAD_GRAYSCALE)
    prime = np.copy(original)

    # checks if image is loaded
    if prime is None:
        print('Obraz się nie otwiera!')
        return -1

    # image preaparation
    canny = cv.Canny(prime, 50, 200, None,
                     3)  # edge (image, treshold1, treshold2, size for sobel opera  detection gaussian filter and gradient)
    gray = cv.cvtColor(canny, cv.COLOR_GRAY2BGR)  # gray scale

    # line detection
    lines = cv.HoughLinesP(canny, 0.1, np.pi / 180, 3, None, 100,
                           10)  # (image,1 px resolution, 1 degrre resolution, treshold, minimum lenghtm max "gap")


    if lines is not None:  # if we found lines

        if (len(lines) > 1000):  # if there was too many lines ommit
            print('Za dużo linii! spróbój ręcznie')
            return -1

        lineslength = len(lines)  # if not, go on

        lenghtP = len(lines)
        obrot = np.copy(prime)

        maxlen = 0
        num1 = 0
        num2 = 0
        (h, w) = prime.shape[:2]

        for i in range(0, len(lines)):  #loop over lines to find axis
            if (lines[i][0][0] < w / 10 and lines[i][0][2] < w / 10 or lines[i][0][0] > w * 9 / 10 and lines[i][0][
                2] > w * 9 / 10 or lines[i][0][1] < h / 10 and lines[i][0][3] < h / 10 or lines[i][0][
                1] > h * 9 / 10 and lines[i][0][3] > h * 9 / 10):  # exclusion of boundaries
                continue

            for j in range(i, len(lines)):
                if (lines[j][0][0] < w / 10 and lines[j][0][2] < w / 10 or lines[j][0][0] > w * 9 / 10 and
                        lines[j][0][2] > w * 9 / 10 or lines[j][0][1] < h / 10 and lines[j][0][3] < h / 10 or
                        lines[j][0][1] > h * 9 / 10 and lines[j][0][3] > h * 9 / 10):  # exclusion of boundaries
                    continue

                if (i == j):# dont check perpedicularity of line to itslef
                    continue

                delxi = lines[i][0][2] - lines[i][0][0]
                delxj = lines[j][0][2] - lines[j][0][0]
                delyi = (lines[i][0][3] - lines[i][0][1])
                delyj = (lines[j][0][3] - lines[j][0][1])

                leni = np.sqrt(np.power(delxi, 2) + np.power(delyi, 2))
                lenj = np.sqrt(np.power(delxj, 2) + np.power(delyj, 2))



                if (np.abs(delxi * delxj + delyi * delyj) < leni * lenj * 0.03):  # perpendicularity test
                    t=0
                    for k in range(0, 2):
                        for l in range(0, 2):

                            if (math.dist((lines[i][0][k * 2], lines[i][0][k * 2 + 1]),
                                          ((lines[j][0][l * 2], lines[j][0][l * 2 + 1]))) < w / 10):
                                t = 1
                                break
                    if (t==0 and maxlen < leni + lenj):
                        maxlen = leni + lenj
                        num1 = i
                        num2 = j

        if (num1 == num2):
            if (num1 == 0):
                print("didn't find any perpeniduclar lines, try lowering treshold")
                return 0
            else:
                print("error: perpendiduclar to self")
                return -1
        t = 0
        for k in range(0, 2):
            for l in range(0, 2):

                if (math.dist((lines[num1][0][k * 2], lines[num1][0][k * 2 + 1]),
                              ((lines[num2][0][l * 2], lines[num2][0][l * 2 + 1]))) < w / 10):
                    t = 1
                    break

        if (t == 1):
            print("ERROR: one of lines is a boundary, try to define axis by hand")  # wykryło krawedzie
            return 1

        l1 = lines[num1][0]
        l2 = lines[num2][0]

        cv.line(original, (l1[0], l1[1]), (l1[2], l1[3]), (0, 0, 255), 3, cv.LINE_AA)  # draw one axis
        cv.line(original, (l2[0], l2[1]), (l2[2], l2[3]), (0, 0, 255), 3, cv.LINE_AA)  # draw second axis


        obroty = rotate_bound(prime, l1, l2)#rotation
        #return obroty
        #cv.imshow("Original", original)#testing
        #cv.imshow("Source0", obroty[0])
        #cv.imshow("Source1", obroty[1])
        #cv.imshow("Source2", obroty[2])
        #cv.imshow("Source", obroty[3])
        #cv.waitKey()
        return obroty

        """  # Define the blue colour we want to find - remember OpenCV uses BGR ordering
                ap = argparse.ArgumentParser()
                ap.add_argument("-i", "--image", help="path to the image")
                args = vars(ap.parse_args())
                # ]
                boundaries = [
                    ([0, 0, 0], [255, 0, 0])  # what to show
                ]

                for (lower, upper) in boundaries:
                # print()
                # create NumPy arrays from the boundaries
                    lower = np.array(lower, dtype="uint8")
                upper = np.array(upper, dtype="uint8")
                # print(lower,"  ",upper)
                #print(cv.inRange(prime, lower, upper))
                mask = cv.inRange(prime, lower, upper)
                output = cv.bitwise_and(prime, prime, mask=mask)

                cv.imshow("images", np.hstack([prime, output]))
                cv.waitKey(0)
                return 0"""

    else:
        print("Not a single line detected! try to do it manualy")
        return 0

#################################################################Probabilistic


# linesP = cv.HoughLinesP(canny, 1, np.pi / 180, 3, None, 50, 10)


# cv.imshow('lul',grayP)
# cv.waitKey(0)#waits for user interaction

#main(r"C:\Users\adams\OneDrive\Pulpit\function_tilted_plot.png")#works
#main(r"C:\Users\adams\OneDrive\Pulpit\tilted.png")#works
#main(r"C:\Users\adams\OneDrive\Pulpit\function_plot.png")#works
#main(r"C:\Users\adams\Downloads\plot2.png")#works
#main(r"C:\Users\adams\Downloads\output-onlinepngtools.png")#works
#main(r"C:\Users\adams\Downloads\simple.png")  # works
#main(r"C:\Users\adams\Downloads\output-onlinepngtools (2).png")#nie
