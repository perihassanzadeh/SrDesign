import cv2 
import numpy as np

topface=[]
leftface = []
frontface = []
rightface=[]
backface=[]
downface = []
vid = cv2.VideoCapture(1)
vid2 = cv2.VideoCapture(2)

def takeImages():
	print("find findFaceColors")
	#open both camera captures
	img_count = 0

	while(vid.isOpened()):
		#read both captures
		ret, frame = vid.read()
		ret2, frame2 = vid2.read()
		cv2.imshow("first", frame)
		cv2.imshow("second", frame2)

		k=cv2.waitKey(1)

		if k%256 == 32:
			#take two pictures from angle
			img_name = "cornerimage{}.png".format(img_count)
			cv2.imwrite(img_name, frame)
			print("{} written!".format(img_name))
			img_count+=1

			img_name = "cornerimage{}.png".format(img_count)
			cv2.imwrite(img_name, frame2)
			print("{} written!".format(img_name))
			img_count+=1

			vid.release()
			vid2.release()
			return


def findFaceColors():
	print("findFaceColors")
	frontX = [175, 230, 300, 175, 230, 300, 170, 230, 300]
	frontY = [175, 120, 50, 225, 175, 110, 300, 250, 200]
	frame = cv2.imread("cornerimage0.png")
	#Get colors from preset coordinates
	for i in range(9):
		x=frontX[i]
		y=frontY[i]
		w=5
		h=5
		avgColor = np.array(cv2.mean(frame[y:y+h, x:x+h])).astype(int)
		color=findCubieColor(avgColor)
		topface.append(color)

	print(topface)
	#return nothing but set face arrays accordingly


def findCubieColor(avgColor):
	print("Find Cubie Color")
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
	if 189 <= avgColor[0] <=250 and 54 <= avgColor[1] <= 95 and 35 <= avgColor[2] <= 97:
		print("blue")
		return "blue"
	elif (345 <= avgColor[0] or avgColor[0] <= 13) and 50 <= avgColor[1] <= 99 and 45 <= avgColor[2] <= 99:
		print("red")
		return "red"
	elif avgColor[0] <= 36 and 60 <= avgColor[1] <= 100 and 60 <= avgColor[2] <= 100:
		print("orange")
		return "orange"
	elif 88<= avgColor[0] <= 162 and 26 <= avgColor[1] <= 99 and 40 <= avgColor[2] <= 91:
		print("green")
		return "green"
	elif 40<= avgColor[0] <= 80 and 32 <= avgColor[1] <= 90 and 44 <= avgColor[2] <= 100:
		print("yellow")
		return "yellow"
	elif avgColor[1] <= 26 and 54 <= avgColor[2]:
		print("white")
		return "white"


def appendFaces():
	print("find findFaceColors")
	#combine all face color states according to koceimba state
	#return one array of entire cube state


def main():
	#take images
	takeImages()

	#find colors from images
	#findFaceColors()
	#append all faces

	#return/print color array

	#optional: call kociemba to solve 


if __name__ == '__main__':
	main()