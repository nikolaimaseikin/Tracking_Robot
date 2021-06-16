from threading import Thread
from picamera.array import PiRGBArray
from picamera import PiCamera
import sys, time
import cv2
import numpy as np
import math

class Tracker(Thread):
    def __init__(self, camera_resolution = (640, 480), camera_angles = (62.2, 48,8)):
        Thread.__init__(self)
        self.lastx = 0
        self.lasty = 0
        self.time = 0
        self.dt = 0
        self.camera_resolution = camera_resolution
        self.center_x = camera_resolution[0] / 2
        self.center_y = camera_resolution[1] / 2
        self.horizontal_angle = camera_angles[0]
        self.vertical_angle = camera_angles[1]
        self.step_angle_horizontal = camera_resolution[0] / camera_angles[0]
        self.step_angle_vertical = camera_resolution[1] / camera_angles[1]
    
    def search(self, img, colorRange, morph_transform = False, blur = False, houghCirclesParameters = (1, 1, 1, 1, 60)):
        h, w = img.shape[:2]
        self.dt = time.clock() - self.time
        self.time = time.clock
        
        hsv_image = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        filtered_image = cv2.inRange(hsv_image, colorRange[0], colorRange[1])
        
        if morph_transform:
            st1 = cv2.getStructuringElement(cv2.MORPH_RECT, (21, 21), (10, 10))
            st2 = cv2.getStructuringElement(cv2.MORPH_RECT, (11, 11), (5, 5))
            filtered_image = cv2.morphologyEx(filtered_image, cv2.MORPH_CLOSE, st1) 
            filtered_image = cv2.morphologyEx(filtered_image, cv2.MORPH_OPEN, st2)
        
        if blur:
            filtered_image = cv2.GaussianBlur(filtered_image, (5, 5), 2)
        
        detected_circles = cv2.HoughCircles(filtered_image, cv2.HOUGH_GRADIENT, 1, houghCirclesParameters[0], param1 = houghCirclesParameters[1],param2 = houghCirclesParameters[2], minRadius = houghCirclesParameters[3], maxRadius = houghCirclesParameters[4])

        if detected_circles is not None:
            detected_circles = np.uint16(np.around(detected_circles))
            filterred_object = None
            maxRadius = 0
            for circle in detected_circles:
                if circle[2] > maxRadius:
                    maxRadius = circle[2]
                    filterred_object = circle

        return filterred_object 

    def showFrame(self, image, filterred_object):
        x,y,r = filterred_object[0], filterred_object[1], filterred_object[2]
        # Нарисуйте окружность круга.
        cv2.circle(image, (x, y), r, (0, 255, 0), 2)
        # Нарисуйте маленький круг (радиус 1), чтобы показать центр.
        cv2.circle(image, (x, y), 1, (0, 0, 255), 3)
        #Вывод значений координат и радиуса на изображение
        cv2.putText(image, str(x), (20,40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        cv2.putText(image, str(y), (40,40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        cv2.putText(image, str(r), (60,40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        cv2.imshow('Frame', image)

    def getShift(self, filterred_object):
        x_shift = 0
        y_shift = 0
        horizontal_turn_angle = 0
        vertical_turn_angle = 0
        #z_shift =0
        x_position = filterred_object[0]
        y_position = filterred_object[1]
        #Запомнить текущее положение (экспериментально)
        self.lastx = x_position
        self.lasty = y_position
        #Получить сдвиг по оси x, относительно координат центра
        if x_position < self.center_x:
            x_shift = -(self.center_x - x_position)
        if x_position > self.center_x:
            x_shift = x_position - self.center_x
        #Получить сдвиг по оси y, относительно координат центра
        if y_position < self.center_y:
            y_shift = -(self.center_y - y_position)
        if y_position > self.center_y:
            y_shift = y_position - self.center_y
        #Преобразовать сдвиг по оси x в угол поворота платформы
        horizontal_turn_angle = x_shift * self.step_angle_horizontal
        #Преобразовать сдвиг по оси y в угол поворота платформы
        vertical_turn_angle = y_shift * self.step_angle_vertical

        return (x_shift, y_shift, horizontal_turn_angle, vertical_turn_angle)

    def getSpeed(self, filterred_object):
        speed = abs(math.sqrt(pow((filterred_object[0] - self.lastx),2) + pow((filterred_object[1] - self.lasty),2)) / self.dt)
        return speed
     


        

        
            
    
        
        
        
        
        

        
            
            
                
                
            
            
            
        
        
        
         
        

