import RPi.GPIO as GPIO
from time import sleep

in3 = 24
in4 = 23
in1 = 21
in2 = 20
enB = 12
enA = 18
GPIO.setmode(GPIO.BCM)

GPIO.setup(in1,GPIO.OUT)
GPIO.setup(in2,GPIO.OUT)
GPIO.setup(in3,GPIO.OUT)
GPIO.setup(in4,GPIO.OUT)
GPIO.setup(enA,GPIO.OUT)
GPIO.setup(enB,GPIO.OUT)

GPIO.output(in1,GPIO.LOW)
GPIO.output(in2,GPIO.HIGH)
GPIO.output(in3,GPIO.LOW)
GPIO.output(in4,GPIO.HIGH)
GPIO.output(enA,GPIO.HIGH)
GPIO.output(enB,GPIO.HIGH)
sleep(2)
GPIO.output(enA,GPIO.LOW)
GPIO.output(enB,GPIO.LOW)
GPIO.cleanup()
