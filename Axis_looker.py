#import packages
import sys
import math
import cv2
import cv2 as cv
import numpy as np
import argparse

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
    original=np.copy(prime)

    #checks if image is loaded
    if prime is None:
        print('Obraz się nie otwiera!')
        return -1

    #przygotowanie obrazu
    canny=cv.Canny(prime,50,200,None,3)#edge (image, treshold1, treshold2, size for sobel opera  detection gaussian filter and gradient
    gray = cv.cvtColor(canny, cv.COLOR_GRAY2BGR)

    #wyszukanie lini
    lines=cv.HoughLinesP(canny, 0.1, np.pi / 180, 3, None, 300, 10)#image resolution (1pixedl)#########################################################

    for i in range(0, len(lines)):#rozczytanie linii
        l = lines[i][0]
        cv.line(gray, (l[0], l[1]), (l[2], l[3]), (0, 0, 255), 3, cv.LINE_AA)
        cv.line(gray, (l[0], l[1]), (l[2], l[3]), (0, 0, 255), 3, cv.LINE_AA)

    if lines is not None:#mamy linnie działamy

        if(len(lines)>1000):#za dużo szkoda czasu
            print('Za dużo linii! spróbój ręcznie')
            return -1

        lineslength=len(lines)#jest ok działamy dalej

        lenghtP = len(lines)
        obrot = np.copy(prime)
        if lines is not None:  # draw lines
            print("lines", len(lines))
            # print(lines)
            maxlen = 0
            num1 = 0
            num2 = 0
            (h, w) = prime.shape[:2]

            #t = 0
            for i in range(0, len(lines)):##sprawdza prostopadłość i długość
                for j in range(i, len(lines)):

                    delxi = lines[i][0][2] - lines[i][0][0]
                    delxj = lines[j][0][2] - lines[j][0][0]
                    delyi = (lines[i][0][3] - lines[i][0][1])
                    delyj = (lines[j][0][3] - lines[j][0][1])

                    leni = np.sqrt(np.power(delxi, 2) + np.power(delyi, 2))
                    lenj = np.sqrt(np.power(delxj, 2) + np.power(delyj, 2))

                    if (np.abs(delxi * delxj + delyi * delyj) < leni * lenj * 0.05):
                        if (maxlen < leni + lenj):
                            maxlen = leni + lenj
                            num1 = i
                            num2 = j

            t=0
            for k in range(0,2):
                for l in range(0,2):

                    if(num1==num2):
                        print("upss znalazło te same linie")
                        return 1

                    if(math.dist((lines[num1][0][k*2],lines[num1][0][k*2+1]),((lines[num2][0][l*2],lines[num2][0][l*2+1])))<w/10):
                        t=1
                        break

            if(t==1):
                print("t1==1 w krótce zostanie poprawione!!!")#wykryło krawedzie
               # return 1

            print("lines  ",lines[num1])
            l1 = lines[num1][0]
            l2 = lines[num2][0]

            cv.line(prime, (l1[0], l1[1]), (l1[2], l1[3]), (0, 0, 255), 3, cv.LINE_AA)
            cv.line(prime, (l2[0], l2[1]), (l2[2], l2[3]), (0, 0, 255), 3, cv.LINE_AA)



        cX=(l1[0]+l1[2]+l2[0]+l2[2])/4
        cY=(l1[1]+l1[3]+l2[1]+l2[3])/4
        prime = cv2.circle(prime, (round(cX),round(cY)), 10, (255, 0, 0), -1)

        tg_phi=(l1[3]-l1[1])/(l2[2]-l2[0])
        phi=math.atan(tg_phi)*180/math.pi


        obroty = (rotate_bound(prime, phi, l1, l2),rotate_bound(prime, phi+90, l1, l2),rotate_bound(prime, phi+180, l1, l2),rotate_bound(prime, phi+270, l1, l2))
        cv.imshow("Original", original)
        cv.imshow("Source", prime)
        #cv.imshow("Standard Hough Line Transform", gray)
        # cv.imshow("Probabilistic Line Transform", grayP)
        cv.imshow("obrocone0", obroty[0])
        cv.imshow("obrocone1", obroty[1])
        cv.imshow("obrocone2", obroty[2])
        cv.imshow("obrocone3", obroty[3])
        # cv.imshow("sdz",prime)
        cv.waitKey()




        # Define the blue colour we want to find - remember OpenCV uses BGR ordering
        ap = argparse.ArgumentParser()
        ap.add_argument("-i", "--image", help="path to the image")
        args = vars(ap.parse_args())
        # load the image


       # boundaries = [
        #    ([128,128,128], [255, 255, 255])
        #]
        boundaries = [
           ([0,0,0], [255, 0, 0])#what to show
        ]

        for (lower, upper) in boundaries:
            #print()
            # create NumPy arrays from the boundaries
            lower = np.array(lower, dtype="uint8")
            upper = np.array(upper, dtype="uint8")
           # print(lower,"  ",upper)
            print(cv.inRange(prime, lower, upper))
            mask=cv.inRange(prime, lower, upper)
            output = cv.bitwise_and(prime, prime, mask=mask)

            cv2.imshow("images", np.hstack([prime, output]))
            cv2.waitKey(0)

        return 0

    else:
        print("Not a single line detected! try to do it manualy")
        return 0

#################################################################Probabilistic


   # linesP = cv.HoughLinesP(canny, 1, np.pi / 180, 3, None, 50, 10)


    #cv.imshow('lul',grayP)
    #cv.waitKey(0)#waits for user interaction

#main(r"C:\Users\adams\OneDrive\Pulpit\function_tilted_plot.png")
#main(r"C:\Users\adams\OneDrive\Pulpit\tilted.png")
#main(r"C:\Users\adams\OneDrive\Pulpit\function_plot.png")
#main(r"C:\Users\adams\Downloads\plot2.png")
#main(r"C:\Users\adams\Downloads\output-onlinepngtools.png")
#main(r"C:\Users\adams\Downloads\simple.png")#tak
main(r"C:\Users\adams\Downloads\output-onlinepngtools (2).png")#nie

