import time
import Adafruit_PCA9685
import RPi.GPIO as GPIO

class Servo():
    def __init__(self, address = 0x40, channel = 0, frequency = 60, min_angle = 0, max_angle = 180, servo_range_angle = 180):
        self.channel = channel
        self.min_pulse_length = 150 # Min pulse length out of 4096
        self.max_pulse_length = 600 # Max pulse length out of 4096
        self.current_angle = 0
        self.address = address
        self.pwm = Adafruit_PCA9685.PCA9685(address)
        self.frequency = frequency
        self.max_angle = max_angle
        self.min_angle = min_angle
        self.servo_range_angle = servo_range_angle
        self.pwm.set_pwm_freq(frequency)
        GPIO.setmode(GPIO.BCM)

    def setPosition(self, angle):
        self.current_angle = angle
        servo_position = round(self.min_pulse_length + (self.current_angle * (self.max_pulse_length - self.min_pulse_length) / self.servo_range_angle))
        self.pwm.set_pwm(self.channel, 0, servo_position)

    def getPosition(self):
        return self.current_angle

    def shift(self, angle_offset):
        new_angle = self.current_angle
        if self.current_angle + angle_offset < self.min_angle:
            new_angle = self.min_angle
        if self.current_angle + angle_offset > self.max_angle:
            new_angle = self.max_angle
        else:
            new_angle = self.current_angle + angle_offset
        self.setPosition(new_angle)

    
            
        
            
        
        
        
        
        
        
        
        
        
    
    
    
