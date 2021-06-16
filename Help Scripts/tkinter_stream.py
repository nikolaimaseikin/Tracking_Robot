import tkinter
from picamera.array import PiRGBArray
from picamera import PiCamera
from PIL import Image
from PIL import ImageTk
import time
import cv2


camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 30
rawCapture = PiRGBArray(camera, size = camera.resolution)
# allow the camera to warmup
time.sleep(0.1)
root = tkinter.Tk()
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
root.mainloop()

