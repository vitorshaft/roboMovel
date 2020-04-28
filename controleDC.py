import RPi.GPIO as GPIO          
from time import sleep

in1 = 24
in2 = 23
en = 25

GPIO.setmode(GPIO.BCM)

GPIO.setup(in1,GPIO.OUT)
GPIO.setup(in2,GPIO.OUT)
GPIO.setup(en,GPIO.OUT)
GPIO.output(in1,GPIO.LOW)
GPIO.output(in2,GPIO.LOW)
GPIO.output(en,GPIO.HIGH)   

GPIO.output(in1,GPIO.HIGH)
sleep(3)
GPIO.output(in1,GPIO.LOW)
GPIO.cleanup()
