import cv2
import numpy as np

def compConts(frame):
	frame2 = frame.copy()

	
	gausBlur = 15
	gaus=10
	blur = cv2.bilateralFilter(cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY), gausBlur, 15, 15)
	#frame2 = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, gaus, 2)
	canny = cv2.Canny(frame2, 50, 150)
	kernel = np.ones((3,3), np.uint8)
	dilated = cv2.dilate(canny, kernel, iterations=4)

	(contours, hierarchy) = cv2.findContours(dilated.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	outArr = []
	index = 0

	for cnt in contours:
		if (hierarchy[0, index, 3] != -1):
			epsilon = (15/100)*cv2.arcLength(cnt, True)
			approx = cv2.approxPolyDP(cnt, epsilon, True)

			area=cv2.contourArea(approx, False)
			cv2.drawContours(frame,[cnt], 0, (0,255,0), 3)
			if(len(approx)==4 and area > 264):
				print("inside")
				x,y,w,h = cv2.boundingRect(cnt)
				avgColor = np.array(cv2.mean(frame[y:y+h, x:x+h])).astype(int)
				cv2.drawContours(frame, [approx], 0, (0,255,0), 3)

		index+=1

	return canny


def main():

	image = cv2.imread("cornerimage0.png")
	newframe = compConts(image)
	cv2.imshow("image", newframe)
	cv2.imshow("first",image)
	cv2.waitKey()


if __name__ == '__main__':
	main()

