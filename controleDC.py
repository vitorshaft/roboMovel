import RPi.GPIO as GPIO          
from time import sleep

in3 = 24
in4 = 23
in1 = 1
in2 = 7
enB = 25
enA = 2
encEsq = 27
encDir = 17

GPIO.setmode(GPIO.BCM)

GPIO.setup(in1,GPIO.OUT)
GPIO.setup(in2,GPIO.OUT)
GPIO.setup(in3,GPIO.OUT)
GPIO.setup(in4,GPIO.OUT)
GPIO.setup(enA,GPIO.OUT)
GPIO.setup(enB,GPIO.OUT)
pwmEsq = GPIO.PWM(25,100)
pwmEsq.start(0)
pwmDir = GPIO.PWM(2,100)
pwmDir.start(0)
GPIO.setup(encEsq,GPIO.IN)
GPIO.setup(encDir,GPIO.IN)


pDir = 0
pEsq = 0

def contadorE():
	global pEsq
	pEsq += 1
	return pEsq
	
def contadorD():
	global pDir
	pDir += 1
	return pDir
	
def esquerda(vazio):
	if GPIO.input(encEsq):
		print (contadorE())
def direita(vazio):
	if GPIO.input(encDir):
		print (contadorD())

def esq(d):
	setPoint = d/15
	while(pEsq <= setPoint):
		#GPIO.output(en,GPIO.HIGH)
		pwmEsq.ChangeDutyCycle(70)
		GPIO.output(in1,GPIO.LOW)
		GPIO.output(in2,GPIO.HIGH)
	#GPIO.output(en,GPIO.HIGH)
	pwmEsq.ChangeDutyCycle(0)
	GPIO.output(in1,GPIO.HIGH)
	GPIO.output(in2,GPIO.HIGH)
	GPIO.cleanup()

def dir(d):
	setPoint = d/15
	while(pDir <= setPoint):
		#GPIO.output(en,GPIO.HIGH)
		pwmDir.ChangeDutyCycle(70)
		GPIO.output(in3,GPIO.LOW)
		GPIO.output(in4,GPIO.HIGH)
	#GPIO.output(en,GPIO.HIGH)
	pwmDir.ChangeDutyCycle(0)
	GPIO.output(in3,GPIO.HIGH)
	GPIO.output(in4,GPIO.HIGH)
	GPIO.cleanup()
		
GPIO.add_event_detect(encEsq, GPIO.BOTH, callback=esquerda)
GPIO.add_event_detect(encDir, GPIO.BOTH, callback=direita)
'''
GPIO.output(in1,GPIO.LOW)
GPIO.output(in2,GPIO.LOW)
GPIO.output(en,GPIO.HIGH)

GPIO.output(in2,GPIO.HIGH)
#sleep(3)
GPIO.output(in2,GPIO.LOW)
'''
esq(60)
dir(60)
#GPIO.cleanup()
