import RPi.GPIO as GPIO          
from time import sleep

in3 = 24
in4 = 23
in1 = 21
in2 = 20
enB = 25
enA = 2
encEsq = 17
encDir = 27

GPIO.setmode(GPIO.BCM)

GPIO.setup(in1,GPIO.OUT)
GPIO.setup(in2,GPIO.OUT)
GPIO.setup(in3,GPIO.OUT)
GPIO.setup(in4,GPIO.OUT)
GPIO.setup(enA,GPIO.OUT)
GPIO.setup(enB,GPIO.OUT)

pwmEsq = GPIO.PWM(2,100)
pwmEsq.start(0)
pwmDir = GPIO.PWM(25,100)
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
		print ("esquerdo: ",contadorE())
def direita(vazio):
	if GPIO.input(encDir):
		print ("direito: ",contadorD())

def esq(d):
	setPoint = d/15
	while(pDir <= setPoint):
		#GPIO.output(en,GPIO.HIGH)
		pwmEsq.ChangeDutyCycle(30)
		GPIO.output(in1,GPIO.LOW)
		GPIO.output(in2,GPIO.HIGH)
	#GPIO.output(en,GPIO.HIGH)
	pwmEsq.ChangeDutyCycle(0)
	GPIO.output(in1,GPIO.HIGH)
	GPIO.output(in2,GPIO.HIGH)
	#GPIO.cleanup()

def dire(d):
	setP = d/15
	while(pEsq <= setP):
		#GPIO.output(en,GPIO.HIGH)
		pwmDir.ChangeDutyCycle(30)
		GPIO.output(in3,GPIO.LOW)
		GPIO.output(in4,GPIO.HIGH)
	#GPIO.output(en,GPIO.HIGH)
	pwmDir.ChangeDutyCycle(0)
	GPIO.output(in3,GPIO.HIGH)
	GPIO.output(in4,GPIO.HIGH)
	#GPIO.cleanup()
def frente(d):
	global pEsq
	global pDir
	pEsq = 0
	pDir = 0
	sp = d/15
	while(pEsq <= sp or pDir <= sp):
		pwmDir.ChangeDutyCycle(50)
		pwmEsq.ChangeDutyCycle(50)
		GPIO.output(in1,GPIO.LOW)
		GPIO.output(in2,GPIO.HIGH)
		GPIO.output(in3,GPIO.LOW)
		GPIO.output(in4,GPIO.HIGH)
	pwmEsq.ChangeDutyCycle(0)
	pwmDir.ChangeDutyCycle(0)
	GPIO.output(in1,GPIO.HIGH)
	GPIO.output(in2,GPIO.HIGH)
	GPIO.output(in3,GPIO.HIGH)
	GPIO.output(in4,GPIO.HIGH)

def esqRad(graus):
	global pDir
	pDir = 0
	sp = graus/7.5
	while(pDir < sp):
		#GPIO.output(en,GPIO.HIGH)
		pwmEsq.ChangeDutyCycle(30)
		GPIO.output(in1,GPIO.LOW)
		GPIO.output(in2,GPIO.HIGH)
	#GPIO.output(en,GPIO.HIGH)
	pwmEsq.ChangeDutyCycle(0)
	GPIO.output(in1,GPIO.HIGH)
	GPIO.output(in2,GPIO.HIGH)

def dirRad(graus):
	global pEsq
	pEsq = 0
	sp = graus/7.5
	while(pEsq < sp):
		#GPIO.output(en,GPIO.HIGH)
		pwmDir.ChangeDutyCycle(30)
		GPIO.output(in3,GPIO.LOW)
		GPIO.output(in4,GPIO.HIGH)
	#GPIO.output(en,GPIO.HIGH)
	pwmDir.ChangeDutyCycle(0)
	GPIO.output(in3,GPIO.HIGH)
	GPIO.output(in4,GPIO.HIGH)
		
		
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
delta = int(input("distancia em mm: "))
esqRad(delta)
sleep(2)
dirRad(delta)
sleep(1)
frente(delta)
GPIO.cleanup()
