import tkinter
#from Servo import Servo
#from Tracker import Tracker
from picamera.array import PiRGBArray
from picamera import PiCamera
from PIL import Image
from PIL import ImageTk
import time
import cv2


target_hsv_color_range  = ((0, 0, 0),(0, 0, 0))

def setColor(level, element, value):
    global target_hsv_color_range
    target_hsv_color_range[level][element] = value

def h_min_event_handler(event):
    value = h_min.get()
    setColor(0, 0, value)

def s_min_event_handler(event):
    value = s_min.get()
    setColor(0, 1, value)

def v_min_event_handler(event):
    value = v_min.get()
    setColor(0, 2, value)

def h_max_event_handler(event):
    value = h_max.get()
    setColor(1, 0, value)

def s_max_event_handler(event):
    value = s_max.get()
    setColor(1, 1, value)

def v_max_event_handler(event):
    value = v_max.get()
    setColor(1, 2, value)
    
def calibration():
    pass

def getNextFrame():
    pass

if __name__ == "name":
    root = Tk()
    root.title('Tracking Robot')
    #tracker = Tracker()
    #servo_h = Servo(channel = 14)
    #servo_v = Servo(channel = 15)
    camera = PiCamera()
    camera.resolution = (640, 480)
    camera.framerate = 30
    rawCapture = PiRGBArray(camera, size = camera.resolution)
    # allow the camera to warmup
    time.sleep(0.1)

   
    #Слайдер для определения нижнего порога тона цвета цветового диапазона для поиска 
    h_min = Scale(root,orient= HORIZONTAL ,length=500,from_=0,to=360,tickinterval=20,resolution=1)
    h_min.bind("<B1-Motion>", h_min_event_handler)
    h_min.pack()
    #Слайдер для определения нижнего порога насыщенности цвета цветового диапазона для поиска 
    s_min = Scale(root,orient= HORIZONTAL ,length=500,from_=0,to=100,tickinterval=20,resolution=1)
    s_min.bind("<B1-Motion>", s_min_event_handler)
    s_min.pack()
    #Слайдер для определения нижнего порога яркости цвета цветового диапазона для поиска 
    s_min = Scale(root,orient= HORIZONTAL ,length=500,from_=0,to=100,tickinterval=20,resolution=1)
    s_min.bind("<B1-Motion>", v_min_event_handler)
    s_min.pack()
    #Слайдер для определения верхнего порога тона цвета цветового диапазона для поиска 
    h_max = Scale(root,orient= HORIZONTAL ,length=500,from_=0,to=360,tickinterval=20,resolution=1)
    h_max.bind("<B1-Motion>", h_max_event_handler)
    h_max.pack()
    #Слайдер для определения верхнего порога насыщенности цвета цветового диапазона для поиска 
    s_max = Scale(root,orient= HORIZONTAL ,length=500,from_=0,to=100,tickinterval=20,resolution=1)
    s_max.bind("<B1-Motion>", s_max_event_handler)
    s_max.pack()
    #Слайдер для определения верхнего порога яркости цвета цветового диапазона для поиска 
    s_max = Scale(root,orient= HORIZONTAL ,length=500,from_=0,to=100,tickinterval=20,resolution=1)
    s_max.bind("<B1-Motion>", v_max_event_handler)
    s_max.pack()

    frame_space = tkinter.Label(root)
    frame_space.pack()

    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        frame = cv2.cvtColor(frame.array, cv2.COLOR_BGR2RGB)
        frame = Image.fromarray(frame)
        frame = ImageTk.PhotoImage(frame)
        frame_space.configure(image = frame)
        frame_space.image = frame
        root.update()
        rawCapture.truncate(0)
        print(target_hsv_color_range)

    root.mainloop()

        
        

    
        
        


   








