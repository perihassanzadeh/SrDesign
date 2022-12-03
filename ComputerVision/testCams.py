#Capture State of Rubik's Cube Outside of Enclosure using Images
#Peri Hassanzadeh
#Last Modified: November 30th, 2022

#Imported Libraries 
import cv2 
import numpy as np
import kociemba
import serial
import time

#Setup Serial Communications and video capture
#ser = serial.Serial(port = 'COM4', baudrate=9600)
vid = cv2.VideoCapture(1)
#vid.set()
#State Arrays (Cube Orientation / Colors)
fullface = []
colors = []


###
# Opens camera capture and takes images of each cube face when space bar pressed 
# Images stored in project directory
###
def takeImages():
	print("Take Images of the Cube")
	print("Show Up, Right, Front, Down, Left, Back")
	#open both camera captures
	img_count = 0

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
			img_name = "side{}image2.png".format(img_count)
			cv2.imwrite(img_name, frame)
			print("{} written!".format(img_name))
			img_count+=1

		#All Images have been taken
		if img_count==6:
			vid.release()
			return


###
# Finds Colors of individual cube face 
# Sets/Appends state arrays accordingly 
###
def findFaceColors():
	print("findFaceColors")
	frontX = [200, 300, 400, 200, 300, 400, 200, 300, 400]
	frontY = [100, 100, 100, 200, 200, 200, 300, 300, 300]
	#Get colors from preset coordinates
	for i in range(6):
		frame = cv2.imread("side{}image2.png".format(i))
		for i in range(9):
			x=frontX[i]
			y=frontY[i]
			w=5
			h=5
			avgColor = np.array(cv2.mean(frame[y:y+h, x:x+h])).astype(int)
			color=findCubieColor(avgColor)
			fullface.append(color)

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
	#while True:
		startT = time.time()
		print("Ready")
		#line = ser.readline()
		takeImages()	
		findFaceColors()
		#append all faces
		moves = solveSeq()
		print(moves)
		exectutionT = time.time()-startT
		print("time = " + str(exectutionT))
		#ser.write(moves.encode())


if __name__ == '__main__':
	main()