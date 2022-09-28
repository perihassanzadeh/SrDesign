import cv2
import numpy as np
from imutils import contours

#Camera Input and User View
camera = cv2.VideoCapture(0)
cv2.namedWindow("test")

#Images Taken
img_counter=0

while True:
	ret, frame = camera.read()
	if not ret: #Count not grab frame
		print("Failed to gramb frame")
		break
	cv2.imshow("test", frame) #Show camera frame to user
	
	k = cv2.waitKey(1)
	if k%256 == 27:
		#Escape pressed
		print("escape hit")
		break
	elif k%256 == 32:
		#space pressed
		img_name = "opencv_frame{}.png".format(img_counter)
		cv2.imwrite(img_name, frame)
		print("{} written!".format(img_name))
		img_counter+=1

camera.release()
cv2.destroyAllWindows()
