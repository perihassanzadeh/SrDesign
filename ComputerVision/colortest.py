import cv2
import numpy as np

vid = cv2.VideoCapture(1)
ret, frame = vid.read()
k=cv2.waitKey(1)
while(True):
        cv2.circle(frame, (100,100), radius=0, color=(0,0,255), thickness=5)
        cv2.circle(frame, (100,150), radius=0, color=(0,0,255), thickness=5)
        cv2.circle(frame, (150,150), radius=0, color=(0,0,255), thickness=5)
        cv2.circle(frame, (150,100), radius=0, color=(0,0,255), thickness=5)
        cv2.imshow('LIVE', frame)
        if k%256 == 32:
                print("Escape Hit")
                outputArr = []
                x=100
                y=100
                w=50
                h=50
                avgColor = np.array(cv2.mean(frame[y:y+h, x:x+h])).astype(int)
                #RGB Value
                #print(avgColor)

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
                if 189 <= avgColor[0] <= 250 and 55 <= avgColor[1] <= 95 and 35 <= avgColor[2] <= 90:
                	print('blue detected at', x, y)
                	outputArr.append('blue')
                elif (345 <= avgColor[0] or avgColor[0] <= 13) and 50 <= avgColor[1] <= 99 and 45 <= avgColor[2] <= 99:
                	print('red detected at', x, y)
                	outputArr.append('red')
                elif avgColor[0] <= 36 and 60 <= avgColor[1] <= 100 and 60 <= avgColor[2] <= 100:
                	print('orange detected at', x, y)
                	outputArr.append('orange')
                elif 88<= avgColor[0] <= 153 and 58 <= avgColor[1] <= 99 and 60 <= avgColor[2] <= 80:
                	print('green detected at ', x, y)
                	outputArr.append('green')
                elif 40<= avgColor[0] <= 80 and 55 <= avgColor[1] <= 90 and 70 <= avgColor[2] <= 100:
                	print('yellow detected at ', x, y)
                	outputArr.append('yellow')
                elif avgColor[1] <= 20 and 90 <= avgColor[2]:
                	print('white detected at ', x, y)
                	outputArr.append('white')