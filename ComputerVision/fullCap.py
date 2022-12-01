import cv2
import numpy as np
import math
img_counter = 0
capture = cv2.VideoCapture(1)

def findCubies(frame):
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

        index += 1

    return frame2;

while (capture.isOpened()):
    ret, frame = capture.read()
    ret2, framecopy = capture.read()
    if ret:
        capture.set(cv2.CAP_PROP_EXPOSURE, -5)
        newFrame = findCubies(frame);

        cv2.imshow("Webcam CaptuSre", frame);
        cv2.imshow("Adaptive Gaussian Threshold", newFrame);
        cv2.imshow("original webcam", framecopy)

        k = cv2.waitKey(1)
        if k%256 == 27:
            print("Escape Hit")
            break
        elif k%256 == 32:
            print("Taking Image")
            img_name = "side{}.png".format(img_counter)
            cv2.imwrite(img_name, framecopy)
            print("{} written!".format(img_name))
            img_counter+=1
    else:
        break

capture.release()
cv2.destroyAllWindows()


#while capture is opened
    #find and show contours
        #if space hit
            #take pic and call func to detect colors
            #return color array of 9
            #append returned array to array 
        #if array size 54 then return full array


