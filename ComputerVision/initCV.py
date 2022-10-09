import cv2
import numpy as np

def main():
	image = cv2.imread("opencv_frame0.png")
	newframe = computeContours(image)
	cv2.imshow('Init w Squares', image)
	cv2.imshow('Final', newframe)
	cv2.waitKey()

def initialimg():
	#Read in image and convert it to gray, add blur
	image = cv2.imread("opencv_frame3.png")
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	blurred = cv2.GaussianBlur(gray, (7, 7), 0)

	cv2.imshow('blur', blurred)

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


def computeContours(frame):
    frame2 = frame.copy()
    #frame2 = cv2.imread("opencv_frame3.png")
    gausBlur = 11
    
    gaus = 7

    blur = cv2.bilateralFilter(cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY), gausBlur, 15, 15)

    frame2 = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, gaus, 2)

    canny = cv2.Canny(frame2, 88, 347)

    cv2.imshow("Canny Edge", canny);

    kernel = np.ones((3,3), np.uint8)
    dilated = cv2.dilate(canny, kernel, iterations=3)

    (contours, hierarchy) = cv2.findContours(dilated.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Index used to remove nested squares.
    index = 0
    for cnt in contours:
        if (hierarchy[0,index,3] != -1):
            epsilon = (15/100)*cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, epsilon, True)

            area = cv2.contourArea(approx, False)

            if (len(approx) == 4 and area > 264):
                # Square detected. Draw onto original image.
                cv2.drawContours(frame, [approx], 0, (0, 255, 0), 3)
        index += 1

    
    #colorDetect(contours, epsilon, approx, area)

    return frame2;


# def colorDetect(contours, epsilon, approx, area):
# 	cnt = contours	
# 	print(cnt[0])

# 	for c in contours:
# 		A1=cv2.contourArea(c)
# 		contour_id = contour_id+1

# 		if A1 < 3000 and A1 > 1000:
# 			perimeter = cv2.arcLength(c, True)



if __name__ == '__main__':
		main()