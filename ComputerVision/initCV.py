import cv2
import numpy as np

#Read in image and convert it to gray, add blur
image = cv2.imread("opencv_frame3.png")
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (3, 3), 0)
canny = cv2.Canny(blurred, 20, 40)

#Dilate image to open up
kernel = np.ones((3,3), np.uint8)
dilated = cv2.dilate(canny, kernel, iterations=2)

#Draw contours on image based on continuous average colors
(contours, hierarchy) = cv2.findContours(dilated.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
cv2.drawContours(image, contours, -1, (0,255,0), 3)

#Show image to user
cv2.imshow('canny', image)
cv2.waitKey()