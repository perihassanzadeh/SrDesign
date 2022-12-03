#Capture State of Rubik's Cube Outside of Enclosure using Images
#Peri Hassanzadeh
#Last Modified: November 30th, 2022

#Imported Libraries 
import cv2 
import numpy as np
import kociemba
import serial

#Setup Serial Communications and video capture
ser = serial.Serial(port = 'COM4', baudrate=9600)
vid = cv2.VideoCapture(1)
#vid.set()
#State Arrays (Cube Orientation / Colors)
fullface = []
front = ['-','-','-','-','F','-','-','-','-']
down = ['-','-','-','-','D','-','-','-','-']
back = ['-','-','-','-','B','-','-','-','-']
up = ['-','-','-','-','U','-','-','-','-']
left = ['-','-','-','-','L','-','-','-','-']
right = ['-','-','-','-','R','-','-','-','-']
colors = []

#Different Steps used to communicate with Motors
step=0
img_count = 0
###
# Opens camera capture and takes images of each cube face when space bar pressed 
# Images stored in project directory
###
def takeImages():
    print("Take Images of the Cube")
    print("Show Up, Right, Front, Down, Left, Back")
    #open both camera captures

    while(vid.isOpened()):
        #Read the Camera Capture
        ret, frame = vid.read()
        retcopy, framecopy = vid.read()
        #Circles for Cube Orientation
        cv2.circle(framecopy,(200,100), radius=0, color=(0,0,255), thickness=5)
        cv2.circle(framecopy, (300,200), radius=0, color=(0,0,255), thickness=5)
        cv2.circle(framecopy, (400,300), radius=0, color=(0,0,255), thickness=5)
        cv2.imshow("first", framecopy)

        #Setup Spacebar Press to take Image
        k=cv2.waitKey(1)
        if k%256 == 32:
            #take two pictures from angle
            img_name = "cornerimage{}.png".format(img_count)
            cv2.imwrite(img_name, frame)
            print("{} written!".format(img_name))
            img_count+=1
            return


###
# Finds Colors of individual cube face 
# Sets/Appends state arrays accordingly 
###
def findFaceColors():
    print("findFaceColors")
    frontX = [175, 230, 300, 175, 230, 300, 170, 230, 300, 370, 450, 510, 370, 450, 510, 390, 470, 525, 180, 255, 360, 280, 325, 440, 380, 400, 480]
    frontY = [175, 120, 50, 225, 175, 110, 300, 250, 200, 40, 110, 155, 110, 175, 215, 200, 250, 300, 365, 330, 275, 400, 355, 330, 420, 400, 365]
    #Get colors from preset coordinates
    for i in range(3):
        frame = cv2.imread("comp{}image.png".format(i))
        for y in range(27):
            x=frontX[y]
            y=frontY[y]
            w=5
            h=5
            avgColor = np.array(cv2.mean(frame[y:y+h, x:x+h])).astype(int)
            color=findCubieColor(avgColor)
            fullface.append(color)
        for z in range(9):
            if z!=4 and i==0:
                front[z] = fullface[0+z]
                right[z]=fullface[9+z]
                down[z]=fullface[18+z]
            elif z!=4 and i==1:
                back[z]=fullface[0+z]
                left[z]=fullface[9+z]
            elif z!=4 and i==2:
                down[z]=[18+z]



    print(fullface)
    print(colors)

###
# Finds individual cubie color on passed in image RGB to HSV Value
# Returns Cubie Color
###
def findCubieColor(avgColor):
    #Convert RGB Value to HSV
    blue = avgColor[0]/255
    green = avgColor[1]/255
    red = avgColor[2]/255
    cmax = max(red, blue, green)
    cmin = min(red, blue, green)
    diff = cmax-cmin
    hue = -1
    saturation = -1

    if(cmax==cmin):
        hue=0
    elif(cmax==red):
        hue = (60*((green-blue)/diff)+360)%360
    elif(cmax==green):
        hue = (60*((blue-red)/diff)+120)%360
    elif(cmax==blue):
        hue = (60*((red-green)/diff)+240)%360

    if(cmax==0):
        saturation=0
    else:
        saturation = (diff/cmax)*100

    value = cmax*100

    avgColor[0], avgColor[1], avgColor[2] = hue, saturation, value
    print(hue, saturation, value)

    #Determine Color based on thresholds
    if 189 <= avgColor[0] <=250 and 35 <= avgColor[1] <= 95 and 35 <= avgColor[2] <= 97:
        print("blue")
        colors.append("blue")
        return 'L'
    elif (345 <= avgColor[0] or avgColor[0] <= 12) and 50 <= avgColor[1] <= 100 and 45 <= avgColor[2] <= 99:
        print("red")
        colors.append("red")
        return 'F'
    elif avgColor[0] <= 36 and 60 <= avgColor[1] <= 100 and 60 <= avgColor[2] <= 100:
        print("orange")
        colors.append("orange")
        return 'B'
    elif 86<= avgColor[0] <= 162 and 26 <= avgColor[1] <= 99 and 38 <= avgColor[2] <= 91:
        print("green")
        colors.append("green")
        return 'R'
    elif 38<= avgColor[0] <= 80 and 32 <= avgColor[1] <= 100 and 44 <= avgColor[2] <= 100:
        print("yellow")
        colors.append("yellow")
        return 'U'
    elif avgColor[1] <= 39 and 54 <= avgColor[2]:
        print("white")
        colors.append("white")
        return 'D'


###
# Appends state array to a string and determines solve sequenec
# Returns Moves Sequence to Solve
###
def solveSeq():
    print("find findFaceColors")
    fullfacee=''
    for item in fullface:
        fullfacee+=item

    print(fullfacee)

    return kociemba.solve(fullfacee)


###
# Takes Images, Finds Face Colors, Solves Cube
# Sends Move Seq to motors via Serial Communication with AtMega
###
def main():
    while True:
        print("Ready")
        step = ser.readline()
        if step==1:
            #take image
            takeImages()
            #move cube
            #firstTurn = "2R 2L 2U R L’ 2U 2R 2L 2U R L’ 2D"
            step=2
            ser.write(step.encode())
        elif step==3:
            #move cube back
            takeImages()
            #revandTurn = "2D' L R' 2U' 2L' 2R' 2U' L R' 2U' 2L' 2R' 2R 2L 2B 2R 2L 2B 2R 2L 2B 2F"
            ser.write(step.encode())
            step=4
        elif step==5:
            #take imgae
            takeImages()
            #finalRevSeq = "2F' 2B' 2L' 2R' 2B' 2L' 2R' 2B' 2L' 2R'"
            ser.write(step.encode())
            step=6
        elif step==7:
            #use images to detect colors
            findFaceColors()
            moves = solveSeq
            print(moves)


if __name__ == '__main__':
    main()