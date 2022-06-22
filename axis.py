"""@file hough_lines.py@brief This program demonstrates line finding with the Hough transform"""
import sys
import math
import cv2 as cv
import numpy as np


def main(*argv):
    #checks argument
    default_file = r'C:\Users\adams\OneDrive\Pulpit\sudoku.png'#rconverts normal string to raw
    if(len(argv) > 0):
        filename = argv[0]
    else:
        print("Nie podano nazwy!")
        return -1

    # Loads an image
    src = cv.imread(cv.samples.findFile(filename))#, cv.IMREAD_GRAYSCALE)

    #checks if image is loaded
    if src is None:
        print('Obraz się nie otwiera!')
        #print('Usage: hough_lines.py [image_name -- default ' + default_file + '] \n')
        return -1

    dst=cv.Canny(src,50,200,None,3)#edge (image, treshold1, treshold2, size for sobel opera  detection gaussian filter and gradient
    cdst = cv.cvtColor(dst, cv.COLOR_GRAY2BGR)
    cdstP = np.copy(cdst)


    lines=cv.HoughLinesP(dst,1,np.pi/180,150,None,0,0)#image resolution (1pixedl)

    if lines is not None:
        if(len(lines)>20):
            print('Za dużo linii! spróbój ręcznie')
            return -1

        lineslength=len(lines)
        pt1array=list()
        pt2array=list()
        pt2minpt1attay=list()


        #imaxdist
        for i in range(0, lineslength):
            rho = lines[i][0][0]
            theta = lines[i][0][1]
            a = math.cos(theta)
            b = math.sin(theta)
            x0 = a * rho
            y0 = b * rho
            pt1array.insert(len(pt1array),((int(x0 + 1000 * (-b)), int(y0 + 1000 * (a)))))
           # pt2array.insert(-1, ((int(x0 - 1000 * (-b)), int(y0 - 1000 * (a)))))
            #pt2minpt1attay.insert(-1,cv.norm(pt2array[-1][0]-pt1array[-1][0],pt2array[-1][1]-pt1array[-1][1]))
            print(pt1array)
          #  print(pt2array)
           # print(pt2minpt1attay)
         #   print(pt2array[-1][0]-pt1array[-1][0])
         #   print(pt2array[-1][1]-pt1array[-1][1])
         #   print(pt2array[-1][0]-pt1array[-1][0]^2+pt2array[-1][1]-pt1array[-1][1]^2)
            print()
           # pt2array[i] = (int(x0 - 1000 * (-b)), int(y0 - 1000 * (a)))
            #dist=cv.norm((pt1[0] - pt2[0],pt1[1] - pt2[1]))
            #cv.line(cdst, pt1, pt2, (0, 0, 255), 3, cv.LINE_AA)#draw a line image start poitn end point color thicknes
    else:
        print("Not a single line detected! try to do it manualy")
        return 0

    linesP = cv.HoughLinesP(dst, 1, np.pi / 180, 50, None, 50, 10)

    if linesP is not None:
        for i in range(0, len(linesP)):
            l = linesP[i][0]
            cv.line(cdstP, (l[0], l[1]), (l[2], l[3]), (0, 0, 255), 3, cv.LINE_AA)

    cv.imshow("Source", src)
    # cv.imshow("Standard Hough Line Transform", cdst)
    # cv.imshow("Probabilistic Line Transform", cdstP)
    #cv.imshow("sdz",src)
    cv.waitKey()
    return 0

    #cv.imshow('lul',cdstP)
    #cv.waitKey(0)#waits for user interaction

main(input('Put image name: '))

