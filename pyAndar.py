import RPi.GPIO as GPIO          
from time import sleep

class mover:
	def __init__(self):
		self.in3 = 24
		self.in4 = 23
		self.in1 = 21
		self.in2 = 20
		self.enB = 25
		self.enA = 2
		self.encEsq = 17
		self.encDir = 27
		
		GPIO.setmode(GPIO.BCM)
		
		GPIO.setup(self.in1,GPIO.OUT)
		GPIO.setup(self.in2,GPIO.OUT)
		GPIO.setup(self.in3,GPIO.OUT)
		GPIO.setup(self.in4,GPIO.OUT)
		GPIO.setup(self.enA,GPIO.OUT)
		GPIO.setup(self.enB,GPIO.OUT)
		
		self.pwmEsq = GPIO.PWM(2,100)
		self.pwmEsq.start(0)
		self.pwmDir = GPIO.PWM(25,100)
		self.pwmDir.start(0)
		GPIO.setup(self.encEsq,GPIO.IN)
		GPIO.setup(self.encDir,GPIO.IN)
		
		GPIO.add_event_detect(self.encEsq, GPIO.BOTH, callback=self.esquerda)
		GPIO.add_event_detect(self.encDir, GPIO.BOTH, callback=self.direita)
		
		self.pDir = 0
		self.pEsq = 0

	def contadorE(self):
		#global self.pEsq
		self.pEsq += 1
		return self.pEsq
		
	def contadorD(self):
		#global self.pDir
		self.pDir += 1
		return self.pDir
		
	def esquerda(self,vazio):
		if GPIO.input(self.encEsq):
			print ("esquerdo: ",self.contadorE())
	def direita(self,vazio):
		if GPIO.input(self.encDir):
			print ("direito: ",self.contadorD())
	
	def esq(self,d):
		self.setPoint = d/15
		while(self.pDir <= self.setPoint):
			#GPIO.output(en,GPIO.HIGH)
			self.pwmEsq.ChangeDutyCycle(30)
			GPIO.output(self.in1,GPIO.LOW)
			GPIO.output(self.in2,GPIO.HIGH)
		#GPIO.output(en,GPIO.HIGH)
		self.pwmEsq.ChangeDutyCycle(0)
		GPIO.output(self.in1,GPIO.HIGH)
		GPIO.output(self.in2,GPIO.HIGH)
		#GPIO.cleanup()
	
	def dire(self,d):
		self.setP = d/15
		while(self.pEsq <= self.setP):
			#GPIO.output(en,GPIO.HIGH)
			self.pwmDir.ChangeDutyCycle(30)
			GPIO.output(self.in3,GPIO.LOW)
			GPIO.output(self.in4,GPIO.HIGH)
		#GPIO.output(en,GPIO.HIGH)
		self.pwmDir.ChangeDutyCycle(0)
		GPIO.output(self.in3,GPIO.HIGH)
		GPIO.output(self.in4,GPIO.HIGH)
		#GPIO.cleanup()
	def frente(self,d):
		#global self.pEsq
		#global self.pDir
		self.pEsq = 0
		self.pDir = 0
		self.sp = d/15
		print(self.sp)
		while(self.pEsq <= self.sp or self.pDir <= self.sp):
			self.pwmDir.ChangeDutyCycle(50)
			self.pwmEsq.ChangeDutyCycle(50)
			print(self.pEsq,self.pDir)
			GPIO.output(self.in1,GPIO.LOW)
			GPIO.output(self.in2,GPIO.HIGH)
			GPIO.output(self.in3,GPIO.LOW)
			GPIO.output(self.in4,GPIO.HIGH)
		self.pwmEsq.ChangeDutyCycle(0)
		self.pwmDir.ChangeDutyCycle(0)
		GPIO.output(self.in1,GPIO.HIGH)
		GPIO.output(self.in2,GPIO.HIGH)
		GPIO.output(self.in3,GPIO.HIGH)
		GPIO.output(self.in4,GPIO.HIGH)
	
	def esqRad(self,graus):
		#global self.pDir
		self.pDir = 0
		self.sp = graus/7.5
		while(self.pDir < self.sp):
			#GPIO.output(en,GPIO.HIGH)
			self.pwmEsq.ChangeDutyCycle(30)
			GPIO.output(self.in1,GPIO.LOW)
			GPIO.output(self.in2,GPIO.HIGH)
		#GPIO.output(en,GPIO.HIGH)
		self.pwmEsq.ChangeDutyCycle(0)
		GPIO.output(self.in1,GPIO.HIGH)
		GPIO.output(self.in2,GPIO.HIGH)
	
	def dirRad(graus):
		#global self.pEsq
		self.pEsq = 0
		self.sp = graus/7.5
		while(self.pEsq < self.sp):
			#GPIO.output(en,GPIO.HIGH)
			self.pwmDir.ChangeDutyCycle(30)
			GPIO.output(self.in3,GPIO.LOW)
			GPIO.output(self.in4,GPIO.HIGH)
		#GPIO.output(en,GPIO.HIGH)
		self.pwmDir.ChangeDutyCycle(0)
		GPIO.output(self.in3,GPIO.HIGH)
		GPIO.output(self.in4,GPIO.HIGH)
		
		

'''
GPIO.output(in1,GPIO.LOW)
GPIO.output(in2,GPIO.LOW)
GPIO.output(en,GPIO.HIGH)

GPIO.output(in2,GPIO.HIGH)
#sleep(3)
GPIO.output(in2,GPIO.LOW)

delta = int(input("distancia em mm: "))
esqRad(delta)
sleep(2)
dirRad(delta)
sleep(1)
frente(delta)
GPIO.cleanup()
'''
