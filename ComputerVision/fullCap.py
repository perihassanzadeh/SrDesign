import cv2
import numpy as np
import math

capture = cv2.VideoCapture(1)

def callback(num):
    return

cv2.namedWindow('Settings', 0)
cv2.createTrackbar('Canny Thres 1', 'Settings', 87, 500, callback)
cv2.createTrackbar('Canny Thres 2', 'Settings', 325, 500, callback)
cv2.createTrackbar('Blur kSize', 'Settings', 10, 100, callback)
cv2.createTrackbar('Blur Sigma X', 'Settings', 100, 100, callback)
cv2.createTrackbar('Dilation Iterations', 'Settings', 3, 20, callback)
cv2.createTrackbar('Blob Area', 'Settings', 260, 1000, callback)

cv2.createTrackbar('Epsilon Percent', 'Settings', 6, 100, callback)
cv2.createTrackbar('Max Value', 'Settings', 255, 255, callback)
cv2.createTrackbar('Block Size', 'Settings', 6, 20, callback)
cv2.createTrackbar('C', 'Settings', 2, 255, callback)
cv2.createTrackbar('Contour R', 'Settings', 0, 255, callback)
cv2.createTrackbar('Contour G', 'Settings', 255, 255, callback)
cv2.createTrackbar('Contour B', 'Settings', 0, 255, callback)
cv2.createTrackbar('Exposure', 'Settings', 5, 12, callback)

def computeContours(frame):
    frame2 = frame.copy()
    #frame2 = cv2.imread("opencv_frame3.png")
    gausBlur = 13
    
    gaus = 21

    blur = cv2.bilateralFilter(cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY), gausBlur, 20, 20)

    frame2 = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, gaus, 2)

    canny = cv2.Canny(frame2, 87, 340)

    cv2.imshow("Canny Edge", canny);

    kernel = np.ones((3,3), np.uint8)
    dilated = cv2.dilate(canny, kernel, iterations=10)

    (contours, hierarchy) = cv2.findContours(dilated.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    outputArr = []
    # Index used to remove nested squares.
    index = 0
    #print(len(contours))
    for cnt in contours:
        if (hierarchy[0,index,3] != -1):
            epsilon = (8/100)*cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, epsilon, True)

            area = cv2.contourArea(approx, False)

            if (len(approx) == 4 and area > 260):
                # Square detected. Draw onto original image.
                x,y,w,h = cv2.boundingRect(cnt)
                #print(x, y)
                avgColor = np.array(cv2.mean(frame[y:y+h, x:x+h])).astype(int)
                #print(avgColor)
                cv2.drawContours(frame, [approx], 0, (0, 255, 0), 3)

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
                face = []
                print(hue, saturation, value)
                if 190 <= avgColor[0] <= 250 and 55 <= avgColor[1] <= 95 and 35 <= avgColor[2] <= 85:
                    print('blue detected at', x, y)
                    outputArr.append('blue')
                elif (345 <= avgColor[0] or avgColor[0] <= 11) and 50 <= avgColor[1] <= 90 and 45 <= avgColor[2] <= 90:
                    print('red detected at', x, y)
                    outputArr.append('red')
                elif avgColor[0] <= 36 and 60 <= avgColor[1] <= 99 and 60 <= avgColor[2] <= 99:
                    print('orange detected at', x, y)
                    outputArr.append('orange')
                elif 100<= avgColor[0] <= 153 and 58 <= avgColor[1] <= 99 and 60 <= avgColor[2] <= 80:
                    print('green detected at ', x, y)
                    outputArr.append('green')
                elif 40<= avgColor[0] <= 80 and 55 <= avgColor[1] <= 90 and 70 <= avgColor[2] <= 100:
                    print('yellow detected at ', x, y)
                    outputArr.append('yellow')
                elif avgColor[1] <= 20 and 90 <= avgColor[2]:
                    print('white detected at ', x, y)
                    outputArr.append('white')

        index += 1

    print(outputArr)
    rev = outputArr[::-1]
    print(rev)
    #red, orange, green, orange, yellow, green, orange, white, blue
    #Online Color Picker w/ HSV vals: https://colorpicker.me/#a0d0bb
    return frame2;

while (capture.isOpened()):
    ret, frame = capture.read()
    img_counter = 0
    if ret:
        capture.set(cv2.CAP_PROP_EXPOSURE, (5)*-1)
        newFrame = computeContours(frame);

        cv2.imshow("Webcam Capture", frame);
        cv2.imshow("Adaptive Gaussian Threshold", newFrame);

        k = cv2.waitKey(1)
        if k%256 == 27:
            print("Escape Hit")
            break
        elif: k%256 == 32:
            print("Taking Image")
            img_name = "side{}.png".format(img_counter)
            cv2.imwrite(img_name, frame)
            print("{} written!".format(img_name))
            img_counter+=1
    else:
        break

capture.release()
cv2.destroyAllWindows()