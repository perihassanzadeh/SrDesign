# Importing the libraries
import cv2
import numpy as np
 
# Initiating the webcam
vid = cv2.VideoCapture(1)
#vid.set(cv2.CAP_PROP_EXPOSURE, -5)
#vid2 = cv2.VideoCapture(0)
img_counter=0
outputArr = []
# Capturing frames and showing as a video
while(True):
    ret, frame = vid.read()
    rett1, framecopy = vid.read()
    #ret2, frame2 = vid2.read()
    #rett2, framecopy2 = vid2.read()
    # Getting the width and height of the feed
    #height = int(vid.get(4))
    #width = int(vid.get(3))

    #Uncomment Corrdinates for Prep
    #Front Face Coordinates
    #Row 1
    cv2.circle(framecopy, (175,175), radius=0, color=(0,0,255), thickness=5)
    cv2.circle(framecopy, (230,120), radius=0, color=(0,0,255), thickness=5)
    cv2.circle(framecopy, (300,50), radius=0, color=(0,0,255), thickness=5)
    # #Row 2
    cv2.circle(framecopy, (175,225), radius=0, color=(0,0,255), thickness=5)
    cv2.circle(framecopy, (230,175), radius=0, color=(0,0,255), thickness=5)
    cv2.circle(framecopy, (300,110), radius=0, color=(0,0,255), thickness=5)
    # #Row 3
    cv2.circle(framecopy, (170,300), radius=0, color=(0,0,255), thickness=5)
    cv2.circle(framecopy, (230,250), radius=0, color=(0,0,255), thickness=5)
    cv2.circle(framecopy, (300,200), radius=0, color=(0,0,255), thickness=5)
    
    #Right Face Coordinates
    #Row 1
    cv2.circle(framecopy, (370,40), radius=0, color=(0,0,255), thickness=5)
    cv2.circle(framecopy, (450,110), radius=0, color=(0,0,255), thickness=5)
    cv2.circle(framecopy, (500,155), radius=0, color=(0,0,255), thickness=5)
    # #Row 2
    cv2.circle(framecopy, (370,110), radius=0, color=(0,0,255), thickness=5)
    cv2.circle(framecopy, (450,175), radius=0, color=(0,0,255), thickness=5)
    cv2.circle(framecopy, (510,215), radius=0, color=(0,0,255), thickness=5)
    # #Row 3
    cv2.circle(framecopy, (390,200), radius=0, color=(0,0,255), thickness=5)
    cv2.circle(framecopy, (470,250), radius=0, color=(0,0,255), thickness=5)
    cv2.circle(framecopy, (525,300), radius=0, color=(0,0,255), thickness=5)

    #Down Face Coordinates
    #Row 1
    cv2.circle(framecopy, (180,365), radius=0, color=(0,0,255), thickness=5)
    cv2.circle(framecopy, (255,330), radius=0, color=(0,0,255), thickness=5)
    cv2.circle(framecopy, (360,275), radius=0, color=(0,0,255), thickness=5)
    # #Row 2
    cv2.circle(framecopy, (280,400), radius=0, color=(0,0,255), thickness=5)
    cv2.circle(framecopy, (325,355), radius=0, color=(0,0,255), thickness=5)
    cv2.circle(framecopy, (440,330), radius=0, color=(0,0,255), thickness=5)
    # #Row 3
    cv2.circle(framecopy, (380,420), radius=0, color=(0,0,255), thickness=5)
    cv2.circle(framecopy, (400,400), radius=0, color=(0,0,255), thickness=5)
    cv2.circle(framecopy, (480,365), radius=0, color=(0,0,255), thickness=5)


    #cv2.circle(framecopy, (200,100), radius=0, color=(0,0,255), thickness=5)
    #cv2.circle(framecopy, (300,100), radius=0, color=(0,0,255), thickness=5)
    #cv2.circle(framecopy, (400,100), radius=0, color=(0,0,255), thickness=5)
    # #Row 2
    #cv2.circle(framecopy, (200,200), radius=0, color=(0,0,255), thickness=5)
    #cv2.circle(framecopy, (300,200), radius=0, color=(0,0,255), thickness=5)
    #cv2.circle(framecopy, (400,200), radius=0, color=(0,0,255), thickness=5)
    # #Row 3
    #cv2.circle(framecopy, (200,300), radius=0, color=(0,0,255), thickness=5)
    #cv2.circle(framecopy, (300,300), radius=0, color=(0,0,255), thickness=5)
    #cv2.circle(framecopy, (400,300), radius=0, color=(0,0,255), thickness=5)

    # Showing the video
    cv2.imshow('LIVE', framecopy)
    #cv2.imshow(' ', frame2)
    # Making sure that we have a key to break the while loop
    # Which checks for the ascii value of the key pressed
    xpos=[175, 230, 300, 175, 230, 300, 170, 230, 300, 370, 450, 510, 370, 450, 510, 390, 470, 525, 180, 255, 360, 280, 325, 440, 380, 400, 480]
    ypos = [175, 120, 50, 225, 175, 110, 300, 250, 200, 40, 110, 155, 110, 175, 215, 200, 250, 300, 365, 330, 275, 400, 355, 330, 420, 400, 365]
    k = cv2.waitKey(1)
    if k%256 == 32:
        outputArr.clear()
        #print("Taking Image")
        #img_name = "side{}.png".format(img_counter)
        #img_name2 = "side{}2.png".format(img_counter)
        #cv2.imwrite(img_name, framecopy)
        #cv2.imwrite(img_name2, framecopy2)
        #print("{} written!".format(img_name))
        #img_counter+=1
        for i in range(27):
            x=xpos[i]
            y=ypos[i]
            w=5
            h=5
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
            if 189 <= avgColor[0] <= 250 and 54 <= avgColor[1] <= 95 and 35 <= avgColor[2] <= 97:
                print('blue detected at', x, y)
                outputArr.append('blue')
            elif (345 <= avgColor[0] or avgColor[0] <= 13) and 50 <= avgColor[1] <= 99 and 45 <= avgColor[2] <= 99:
                print('red detected at', x, y)
                outputArr.append('red')
            elif avgColor[0] <= 36 and 60 <= avgColor[1] <= 100 and 60 <= avgColor[2] <= 100:
                print('orange detected at', x, y)
                outputArr.append('orange')
            elif 88<= avgColor[0] <= 162 and 26 <= avgColor[1] <= 99 and 40 <= avgColor[2] <= 91:
                print('green detected at ', x, y)
                outputArr.append('green')
            elif 40<= avgColor[0] <= 80 and 32 <= avgColor[1] <= 90 and 44 <= avgColor[2] <= 100:
                print('yellow detected at ', x, y)
                outputArr.append('yellow')
            elif avgColor[1] <= 26 and 54 <= avgColor[2]:
                print('white detected at ', x, y)
                outputArr.append('white')
                print(outputArr)
        print(outputArr)


# At last release the camera
vid.release()
cv2.destroyAllWindows()