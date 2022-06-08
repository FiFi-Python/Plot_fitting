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


    #przygotowanie obrazu
    canny=cv.Canny(prime,50,200,None,3)#edge (image, treshold1, treshold2, size for sobel opera  detection gaussian filter and gradient
    gray = cv.cvtColor(canny, cv.COLOR_GRAY2BGR)
    grayP = np.copy(gray)

    #wyszukanie lini
    lines=cv.HoughLinesP(canny, 1, np.pi / 180, 3, None, 300, 10)#image resolution (1pixedl)#########################################################

    for i in range(0, len(lines)):#rozczytanie linii
        l = lines[i][0]
        #cv.line(gray, (l[0], l[1]), (l[2], l[3]), (0, 0, 255), 3, cv.LINE_AA)
        #cv.line(gray, (l[0], l[1]), (l[2], l[3]), (0, 0, 255), 3, cv.LINE_AA)
        #print(l[0],"  ",l[2])
       # if(min>l[0]):
        #    min=l[0]
       # if(max<l[2]):
        #    max=l[2]
    #print(min,"  ",max)


    if lines is not None:#mamy linnie działamy

        if(len(lines)>1000):#za dużo szkoda czasu
            print('Za dużo linii! spróbój ręcznie')
            return -1


        lineslength=len(lines)#jest ok działamy dalej
        pt1array=list()
        pt2array=list()
        #pt2minpt1attay=list()

        #imaxdist
        #for i in range(0, lineslength):
          #  rho = lines[i][0][0]
         #   theta = lines[i][0][1]
         #   a = math.cos(theta)
        #    b = math.sin(theta)
        #    x0 = a * rho
        #    y0 = b * rho
        #    pt1array.insert(len(pt1array),((int(x0 + 1000 * (-b)), int(y0 + 1000 * (a)))))
        #    pt2array.insert(len(pt2array), ((int(x0 - 1000 * (-b)), int(y0 - 1000 * (a)))))

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
                if (lines[i][0][0] < w / 10 and lines[i][0][2] < w / 10 or lines[i][0][0] > w * 9 / 10 and lines[i][0][
                    2] > w * 9 / 10 or lines[i][0][1] < h / 10 and lines[i][0][3] < h / 10 or lines[i][0][
                    1] > h * 9 / 10 and lines[i][0][3] > h * 9 / 10):#wykluczenie krawedzi
                    continue
                    print("1")
                for j in range(i, len(lines)):
                    if (lines[j][0][0] < w / 10 and lines[j][0][2] < w / 10 or lines[j][0][0] > w * 9 / 10 and
                            lines[j][0][2] > w * 9 / 10 or lines[j][0][1] < h / 10 and lines[j][0][3] < h / 10 or
                            lines[j][0][1] > h * 9 / 10 and lines[j][0][3] > h * 9 / 10):#wykluczenie krawedzi
                        continue
                        print("1")


                  #  for k in range(0,2):
                   #     for l in range(0,2):
                    #        if(math.dist((lines[i][0][k*2],lines[i][0][k*2+1]),((lines[i][0][l*2],lines[i][0][l*2+1])))<w*9/10):
                    #            print("")
                              #  t=1
                              #  break
                    #if(t==1):
                     #   break
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

                #if(t==1):#wykryło krawędź
                 #   print("t1 w krotce zostanie poprawione!!!")
                  #  return 1

            t=0
            for k in range(0,2):
                for l in range(0,2):
                    #print(k*2," ",k*2+1," ",l*2," ",l*2+1," ",math.dist((lines[i][0][k*2],lines[i][0][k*2+1]),((lines[j][0][l*2],lines[j][0][l*2+1]))))
                    if(math.dist((lines[i][0][k*2],lines[i][0][k*2+1]),((lines[l][0][l*2],lines[j][0][l*2+1])))<w*1/100):
                        t=1
                        break

            if(t==1):
                print("t1==1 w krótce zostanie poprawione!!!")#wykryło krawedzie
                return 1

            l1 = lines[num1][0]
            l2 = lines[num2][0]

            cv.line(prime, (l1[0], l1[1]), (l1[2], l1[3]), (0, 0, 255), 3, cv.LINE_AA)
            cv.line(prime, (l2[0], l2[1]), (l2[2], l2[3]), (0, 0, 255), 3, cv.LINE_AA)

            print("l1 ",l1,"   l2",l2)
        (h, w) = prime.shape[:2]
        print(h,"  ",w)
        prime = cv2.circle(prime, (425, 425), 1, (255, 0, 0), 10)#środki obrazów i środki osi się nie pokrywają :/

        obrot = rotate_bound(prime, 45, l1, l2)
        cv.imshow("Source", prime)
        # cv.imshow("Standard Hough Line Transform", gray)
        # cv.imshow("Probabilistic Line Transform", grayP)
        cv.imshow("obrocone", obrot)
        # cv.imshow("sdz",prime)
        cv.waitKey()

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
main(r"C:\Users\adams\Downloads\plot2.png")
#main(r"C:\Users\adams\Downloads\output-onlinepngtools.png")
