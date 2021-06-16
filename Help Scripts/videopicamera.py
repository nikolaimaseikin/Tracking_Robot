# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import numpy as np   


def nothing(*arg):
    pass
# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 30
rawCapture = PiRGBArray(camera, size = camera.resolution)
# allow the camera to warmup
time.sleep(0.1)

cv2.namedWindow( "Color Settings" ) # создаем окно настроек
cv2.createTrackbar('h1', 'Color Settings', 0, 255, nothing)
cv2.createTrackbar('s1', 'Color Settings', 0, 255, nothing)
cv2.createTrackbar('v1', 'Color Settings', 0, 255, nothing)
cv2.createTrackbar('h2', 'Color Settings', 255, 255, nothing)
cv2.createTrackbar('s2', 'Color Settings', 255, 255, nothing)
cv2.createTrackbar('v2', 'Color Settings', 255, 255, nothing)
cv2.createTrackbar('arg2', 'Color Settings', 10, 255, nothing)
cv2.createTrackbar('p1', 'Color Settings', 70, 255, nothing)
cv2.createTrackbar('p2', 'Color Settings', 10, 255, nothing)
cv2.createTrackbar('minR', 'Color Settings', 1, 255, nothing)
cv2.createTrackbar('maxR', 'Color Settings', 35, 255, nothing)
crange = [0,0,0,0,0,0,0,0,0]

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    h1 = cv2.getTrackbarPos('h1', 'Color Settings')
    s1 = cv2.getTrackbarPos('s1', 'Color Settings')
    v1 = cv2.getTrackbarPos('v1', 'Color Settings')
    h2 = cv2.getTrackbarPos('h2', 'Color Settings')
    s2 = cv2.getTrackbarPos('s2', 'Color Settings')
    v2 = cv2.getTrackbarPos('v2', 'Color Settings')
    arg2 = cv2.getTrackbarPos('arg2', 'Color Settings')
    p1 = cv2.getTrackbarPos('p1', 'Color Settings')
    p2 = cv2.getTrackbarPos('p2', 'Color Settings')
    minR = cv2.getTrackbarPos('minR', 'Color Settings')
    maxR = cv2.getTrackbarPos('maxR', 'Color Settings')
    # grab the raw NumPy array representing the image, then initialize the timestamp
     # and occupied/unoccupied text
    image = frame.array
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    # применяем цветовой фильтр
    thresh = cv2.inRange(hsv, (h1, s1, v1), (h2, s2, v2))
    cv2.imshow('Color Mask', thresh)
    # Применить преобразование Хафа на размытое изображение.
    detected_circles = cv2.HoughCircles(thresh, cv2.HOUGH_GRADIENT, 1, arg2, param1 = p1,param2 = p2, minRadius = minR, maxRadius = maxR)
    # Нарисуйте круги, которые обнаружены
    count = 0
    if detected_circles is not None:
        # Преобразовать параметры круга a, b и r в целые числа.
        detected_circles = np.uint16(np.around(detected_circles))
        for pt in detected_circles[0, :]:
            count += 1
            a, b, r = pt[0], pt[1], pt[2]
            print("x = %f ; y = %f" % (pt[0], pt[1]) )
            # Нарисуйте окружность круга.
            cv2.circle(image, (a, b), r, (0, 255, 0), 2)
            # Нарисуйте маленький круг (радиус 1), чтобы показать центр.
            cv2.circle(image, (a, b), 1, (0, 0, 255), 3)  
    #print("Окружностей найдено: " + str(count))
    cv2.putText(image, str(count), (20,40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    cv2.imshow('Frame', image)
    key = cv2.waitKey(1) & 0xFF
    # clear the stream in preparation for the next frame
    rawCapture.truncate(0)
    # if the `q` key was pressed, break from the loop
    if key == ord("q"):
        break
    
cv2.destroyAllWindows()


    
