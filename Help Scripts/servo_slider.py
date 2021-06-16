from __future__ import division
from tkinter import*
import time
import Adafruit_PCA9685
import RPi.GPIO as GPIO

servo_min = 150  # Min pulse length out of 4096
servo_max = 600  # Max pulse length out of 4096
channel_slider1 = 15
channel_slider2 = 14
    
def setAngle(channel, angle):
    global pwm
    servo_position = round(150 + (angle * 2.5))
    pwm.set_pwm(channel, 0, servo_position)

def slider1(event):
    angle = scal1.get()
    print("Motion Number",str(angle))
    setAngle(channel_slider1, angle)

def slider2(event):
    angle = scal2.get()
    print("Motion Number",str(angle))
    setAngle(channel_slider2, angle)

def slider3(event):
    position = scal3.get()
    pwm.set_pwm(channel_slider1, 0, position)

# Initialise the PCA9685 using the default address (0x40).
pwm = Adafruit_PCA9685.PCA9685()
pwm.set_pwm_freq(60)
GPIO.setmode(GPIO.BCM)

root = Tk()
root.title('Servo Control')


try:
    scal1 = Scale(root,orient= HORIZONTAL ,length=500,from_=0,to=180,tickinterval=20,resolution=1)
    scal1.bind("<B1-Motion>",slider1)
    scal1.pack()
    scal2 = Scale(root,orient= HORIZONTAL ,length=500,from_=0,to=180,tickinterval=20,resolution=1)
    scal2.bind("<B1-Motion>",slider2)
    scal2.pack()
    scal3 = Scale(root,orient= HORIZONTAL ,length=500,from_= 150,to=600,tickinterval=20,resolution=1)
    scal3.bind("<B1-Motion>",slider3)
    scal3.pack()
except:
    GPIO.cleanup()
finally:
    GPIO.cleanup()

root.mainloop()