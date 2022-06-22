# import packages
import sys
import math
import cv2 as cv
import numpy as np
import argparse




def main(*argv):
    if (len(argv) > 2):
       # filename = argv[0]
        original = argv[0]
        cX=argv[1]
        cY=argv[2]
    else:
        print("No file name given")
        return -1

        # Loads an image
    #original = cv.imread(cv.samples.findFile(filename))  # , cv.IMREAD_GRAYSCALE)

    prime = np.copy(original)

    if prime is None:
        print('Obraz się nie otwiera!')
        return -1


#########
   # boundaries = [([0, 0, 0], [255, 255,255])] # gray scale that we accept
    gray = cv.cvtColor(prime, cv.COLOR_BGR2GRAY)  # converting to grayscale
    prime1 = np.copy(gray)#works on copy

    mask = cv.inRange(prime1,0,200)# lower, upper)
    output = cv.bitwise_and(prime1, prime1, mask=mask)#show only given gray scale

    coord = cv.findNonZero(output)#coordinates


    for i in range(0,len(coord)):
    #    if(i%100==0):
        if(coord[i][0][0]>cX+5 or coord[i][0][0]<cX-5):
            if((coord[i][0][1]>cX+5 or coord[i][0][1]<cY-5)):
                prime = cv.circle(prime, (round(coord[i][0][0]), round(coord[i][0][1])), 1, (255, 0, 0), -1)

    # return cv.imshow("Output images", prime)
    #cv.waitKey(0)
    return [prime, coord]

#original = cv.imread(r"C:\Users\adams\OneDrive\Pulpit\function_tilted_plot.png")
#main(original,100,100)
# , cv.IMREAD_GRAYSCALE)
#original = cv.imread(r"{}".format("C:\Users\Lenovo\Desktop\aaa\function_tilted_plot.png"))
# main(original,100,100)#main(r"C:\Users\adams\OneDrive\Pulpit\tilted.png")#works
#main(r"C:\Users\adams\OneDrive\Pulpit\function_plot.png")#works
#main(r"C:\Users\adams\Downloads\plot2.png", 100, 100)#works
#main(r"C:\Users\adams\Downloads\output-onlinepngtools.png")#works
#main(r"C:\Users\adams\Downloads\output-onlinepngtools (2).png")#nie
