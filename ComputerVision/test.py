import cv2
import numpy as np
import math

capture = cv2.VideoCapture(1)

def callback(num):
    return

cv2.namedWindow('Settings', 0)
cv2.createTrackbar('Canny Thres 1', 'Settings', 87, 500, callback)
cv2.createTrackbar('Canny Thres 2', 'Settings', 325, 500, callback)
cv2.createTrackbar('Blur kSize', 'Settings', 10, 100, callback)
cv2.createTrackbar('Blur Sigma X', 'Settings', 100, 100, callback)
cv2.createTrackbar('Dilation Iterations', 'Settings', 3, 20, callback)
cv2.createTrackbar('Blob Area', 'Settings', 260, 1000, callback)

cv2.createTrackbar('Epsilon Percent', 'Settings', 6, 100, callback)
cv2.createTrackbar('Max Value', 'Settings', 255, 255, callback)
cv2.createTrackbar('Block Size', 'Settings', 6, 20, callback)
cv2.createTrackbar('C', 'Settings', 2, 255, callback)
cv2.createTrackbar('Contour R', 'Settings', 0, 255, callback)
cv2.createTrackbar('Contour G', 'Settings', 255, 255, callback)
cv2.createTrackbar('Contour B', 'Settings', 0, 255, callback)
cv2.createTrackbar('Exposure', 'Settings', 5, 12, callback)

def computeContours(frame):
    frame2 = frame.copy()

    gausBlur = cv2.getTrackbarPos('Blur kSize', 'Settings')
    if gausBlur == 0:
        gausBlur = 1;
    else:
        count = gausBlur % 2 
        if (count == 0):
            gausBlur += 1
    
    gaus = cv2.getTrackbarPos('Block Size', 'Settings')
    if gaus < 3:
        gaus = 3;
    else:
        count = gaus % 2 
        if (count == 0):
            gaus += 1

    blur = cv2.bilateralFilter(cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY),
        gausBlur,
        cv2.getTrackbarPos('Blur Sigma X', 'Settings'),
        cv2.getTrackbarPos('Blur Sigma X', 'Settings'))

    frame2 = cv2.adaptiveThreshold(blur,
        cv2.getTrackbarPos('Max Value', 'Settings'),
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY_INV,
        gaus,
        cv2.getTrackbarPos('C', 'Settings'))

    canny = cv2.Canny(
        frame2,
        cv2.getTrackbarPos('Canny Thres 1', 'Settings'),
        cv2.getTrackbarPos('Canny Thres 2', 'Settings'))

    cv2.imshow("Canny Edge", canny);

    kernel = np.ones((3,3), np.uint8)
    dilated = cv2.dilate(canny, kernel, iterations=cv2.getTrackbarPos('Dilation Iterations', 'Settings'))

    (contours, hierarchy) = cv2.findContours(dilated.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Index used to remove nested squares.
    index = 0
    for cnt in contours:
        if (hierarchy[0,index,3] != -1):
            epsilon = (cv2.getTrackbarPos('Epsilon Percent', 'Settings')/100)*cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, epsilon, True)

            area = cv2.contourArea(approx, False)

            if (len(approx) == 4 and area > cv2.getTrackbarPos('Blob Area', 'Settings')):
                # Square detected. Draw onto original image.
                cv2.drawContours(frame, [approx], 0, (cv2.getTrackbarPos('Contour B', 'Settings'), cv2.getTrackbarPos('Contour G', 'Settings'), cv2.getTrackbarPos('Contour R', 'Settings')), 3)
        index += 1

    return frame2;

while (capture.isOpened()):
    ret, frame = capture.read()

    if ret:
        capture.set(cv2.CAP_PROP_EXPOSURE, (cv2.getTrackbarPos('Exposure', 'Settings')+1)*-1)
        newFrame = computeContours(frame);

        cv2.imshow("Webcam Capture", frame);
        cv2.imshow("Adaptive Gaussian Threshold", newFrame);

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break

capture.release()
cv2.destroyAllWindows()