#import packages
import sys
import math
import cv2
import cv2 as cv
import numpy as np

#import functions
from rotate_bound import rotate_bound


def main(*argv):
    if(len(argv) > 0):
        filename = argv[0]
    else:
        print("Nie podano nazwy!")
        return -1

    # Loads an image
    prime = cv.imread(cv.samples.findFile(filename))#, cv.IMREAD_GRAYSCALE)

    #checks if image is loaded
    if prime is None:
        print('Obraz się nie otwiera!')
        #print('Usage: hough_lines.py [image_name -- default ' + default_file + '] \n')
        return -1
    #width=prime.shape[0]########################################################################################
    #print(width)
    canny=cv.Canny(prime,50,200,None,3)#edge (image, treshold1, treshold2, size for sobel opera  detection gaussian filter and gradient
    gray = cv.cvtColor(canny, cv.COLOR_GRAY2BGR)
    grayP = np.copy(gray)

    ######################clasic
    lines=cv.HoughLinesP(canny,1,np.pi/180,150,None,0,0)#image resolution (1pixedl)#########################################################

    for i in range(0, 1):
        l = lines[i][0]
        cv.line(gray, (l[0], l[1]), (l[2], l[3]), (0, 0, 255), 3, cv.LINE_AA)
    if lines is not None:
        if(len(lines)>200):
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
            pt2array.insert(len(pt2array), ((int(x0 - 1000 * (-b)), int(y0 - 1000 * (a)))))

            #pt2minpt1attay.insert(;en(pt2minpt1attay),cv.norm(pt2array[-1][0]-pt1array[-1][0],pt2array[-1][1]-pt1array[-1][1]))
            #print(pt1array)
           # print(pt2array)
            #print(pt2minpt1attay)
         #   print(pt2array[-1][0]-pt1array[-1][0])
         #   print(pt2array[-1][1]-pt1array[-1][1])
         #   print(pt2array[-1][0]-pt1array[-1][0]^2+pt2array[-1][1]-pt1array[-1][1]^2)
            #print()
           # pt2array[i] = (int(x0 - 1000 * (-b)), int(y0 - 1000 * (a)))
            #dist=cv.norm((pt1[0] - pt2[0],pt1[1] - pt2[1]))
            #cv.line(grayP, pt1, pt2, (0, 0, 255), 3, cv.LINE_AA)#draw a line image start poitn end point color thicknes

    else:
        print("Not a single line detected! try to do it manualy")
        return 0

#################################################################Probabilistic


    linesP = cv.HoughLinesP(canny, 1, np.pi / 180, 3, None, 50, 10)
    lenghtP=len(linesP)
    obrot=np.copy(prime)
    if linesP is not None:#draw lines
        print("linesP", len(linesP))
        #print(linesP)
        maxlen=0
        num1=0
        num2=0
        for i in range(0, len(linesP)):
            for j in range(i,len(linesP)):
                delxi=linesP[i][0][2]-linesP[i][0][0]
                delxj=linesP[j][0][2]-linesP[j][0][0]
                delyi=(linesP[i][0][3]-linesP[i][0][1])
                delyj=(linesP[j][0][3]-linesP[j][0][1])
                leni=np.sqrt(np.power(delxi,2)+np.power(delyi,2))
                lenj=np.sqrt(np.power(delxj,2)+np.power(delyj,2))
                if(np.abs(delxi*delxj+delyi*delyj)<leni*lenj*0.05):
                    if(maxlen<leni+lenj):
                        maxlen=leni+lenj
                        num1=i
                        num2=j
        l1=linesP[num1][0]
        l2=linesP[num2][0]
        cv.line(prime, (l1[0], l1[1]), (l1[2], l1[3]), (0, 0, 255), 3, cv.LINE_AA)
        cv.line(prime, (l2[0], l2[1]), (l2[2], l2[3]), (0, 0, 255), 3, cv.LINE_AA)

    obrot = rotate_bound(prime, 0,l1,l2)
    cv.imshow("Source", prime)
    #cv.imshow("Standard Hough Line Transform", gray)
    #cv.imshow("Probabilistic Line Transform", grayP)
    cv.imshow("obrocone", obrot)
    #cv.imshow("sdz",prime)
    cv.waitKey()
    return 0

    #cv.imshow('lul',grayP)
    #cv.waitKey(0)#waits for user interaction

#main(r"C:\Users\adams\OneDrive\Pulpit\function_tilted_plot.png")
main(r"C:\Users\adams\OneDrive\Pulpit\tilted.png")
