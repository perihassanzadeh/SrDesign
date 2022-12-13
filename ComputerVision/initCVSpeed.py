import cv2
import numpy as np
from operator import itemgetter
capture = cv2.VideoCapture(1)

def main():
    image = cv2.imread("side0image2.png")
    newframe = computeContours(image)
    cv2.imshow('Init w Squares', image)
    cv2.imshow('Final', newframe)
    cv2.waitKey()


def computeContours(frame):
    frame2 = frame.copy()
    gausBlur = 13
    gaus = 9
    blur = cv2.bilateralFilter(cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY), gausBlur, 20, 20)
    frame2 = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, gaus, 2)
    canny = cv2.Canny(frame2, 87, 340)
    cv2.imshow("Canny Edge", canny);
    kernel = np.ones((3,3), np.uint8)
    dilated = cv2.dilate(canny, kernel, iterations=4)
    (contours, hierarchy) = cv2.findContours(dilated.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    outputArr = []

    # Index used to remove nested squares.
    index = 0
    for cnt in contours:
        if (hierarchy[0,index,3] != -1):
            epsilon = (8/100)*cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, epsilon, True)
            area = cv2.contourArea(approx, False)

            if (len(approx) == 4 and area > 260):
                # Square detected. Draw onto original image.
                x,y,w,h = cv2.boundingRect(cnt)
                avgColor = np.array(cv2.mean(frame[y:y+h, x:x+h])).astype(int)
                #RGB Value
                #print(avgColor)
                cv2.drawContours(frame, [approx], 0, (0, 255, 0), 3)

                #RGB to HSV
                blue = avgColor[0]/255
                green = avgColor[1]/255
                red = avgColor[2]/255
                cmax =max(red, blue, green)
                cmin = min(red, blue, green)
                diff = cmax - cmin
                hue =-1
                saturation = -1

                if(cmax==cmin):
                    hue=0
                elif(cmax==red):
                    hue = (60*((green-blue)/diff)+360)%360
                elif(cmax==green):
                    hue = (60*((blue-red)/diff)+120)%360
                elif(cmax == blue):
                    hue = (60*((red-green)/diff)+240)%360

                if(cmax==0):
                    saturation=0
                else:
                    saturation=(diff/cmax)*100

                value = cmax*100
                avgColor[0], avgColor[1], avgColor[2] = hue, saturation, value
                print(hue, saturation, value)
                if 189 <= avgColor[0] <= 250 and 54 <= avgColor[1] <= 95 and 35 <= avgColor[2] <= 97:
                    print('blue detected at', x, y)
                    temp = [x, y, 'blue']
                    outputArr.append(temp)
                elif (345 <= avgColor[0] or avgColor[0] <= 13) and 50 <= avgColor[1] <= 99 and 45 <= avgColor[2] <= 99:
                    print('red detected at', x, y)
                    temp = [x, y, 'red']
                    outputArr.append(temp)
                elif avgColor[0] <= 36 and 60 <= avgColor[1] <= 100 and 60 <= avgColor[2] <= 100:
                    print('orange detected at', x, y)
                    temp = [x, y, 'orange']
                    outputArr.append(temp)
                elif 88<= avgColor[0] <= 162 and 26 <= avgColor[1] <= 99 and 40 <= avgColor[2] <= 91:
                    print('green detected at ', x, y)
                    temp = [x, y, 'green']
                    outputArr.append(temp)
                elif 40<= avgColor[0] <= 80 and 32 <= avgColor[1] <= 90 and 44 <= avgColor[2] <= 100:
                    print('yellow detected at ', x, y)
                    temp = [x, y, 'yellow']
                    outputArr.append(temp)
                elif avgColor[1] <= 26 and 54 <= avgColor[2]:
                    print('white detected at ', x, y)
                    temp = [x, y, 'white']
                    outputArr.append(temp)
                else:
                    outputArr.append("none")


        index += 1

    #print(outputArr)
    #Reverse Array
    rev = outputArr[::-1]
    print(rev)

    #top = rev[0]+rev[1]+rev[2]
    #mid = rev[3]+rev[4]
    #bot = rev[5]+rev[6]+rev[7]

    #print(top)
    #print(mid)
    #print(bot)

    #topfinal = sorted(top, key=itemgetter(0))
    #midfinal = sorted(mid, key=itemgetter(0))
    #botfinal=sorted(bot, key=itemgetter(0))

    #finalll=topfinal[0][3]+topfinal[1][3]+topfinal[2][3]+midfinal[0][3]+midfinal[1][3]+botfinal[0][3]+botfinal[1][3]+botfinal[2][3]
    #print(finalll)
    #Online Color Picker w/ HSV vals: https://colorpicker.me/#a0d0bb
    return frame2;


if __name__ == '__main__':
        main()