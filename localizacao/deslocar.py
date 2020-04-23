import math
import time
import stepper
import locRobo

class deslocar:
	self.local = locRobo.loc()

	self.mover = stepper.andar()
	def __init__(self):
		pass
	def rastrear(d,ang):	#desloca o robo em d na direcao ang (graus)
		self.ler = self.local.readLoc('locRobo.json')
		self.dd = d/10
		self.mover.dirAx(ang)
		self.deltaang = ler[4]+ang
		time.sleep(5)
		for i in range(int(dd+1)):
			self.mover.tras(10)
			self.P = local.readLoc('locRobo.json')
			self.deltay = math.sin(math.radians(ang))*10
			self.deltax = math.cos(math.radians(ang))*10
			self.seno = math.sin(math.radians(ang))
			self.cosseno = math.cos(math.radians(ang))
			self.xf = self.P[2]+self.deltax
			self.yf = self.P[3]+self.deltay
			
			local.writeLoc('locRobo.json',xf,yf,seno,cosseno,deltaang)
		
		
	def pipf(x,y):	#desloca o robo ate o ponto (x,y)
		self.P = local.readLoc('locRobo.json')
		self.s = self.P[0]
		self.c = self.P[1]
		self.deltax = x-self.P[2]
		self.deltay = y-self.P[3]
		self.teta = self.P[4]
		self.distancia = math.hypot(self.deltax,self.deltay)
		self.tg = self.deltay/self.deltax
		self.beta = math.atan(self.tg)
		self.ang = math.degrees(self.beta)
		
		
		if self.deltay > 0 and self.deltax > 0:
			self.deltateta = self.ang-self.teta
			self.mover.esqAx(self.deltateta)
		elif self.deltay > 0 and self.deltax < 0:
			self.deltateta = self.ang*(-1)+90-self.teta
			self.mover.esqAx(self.deltateta)
		elif self.deltay < 0 and self.deltax < 0:
			self.deltateta = self.ang+180-self.teta
			if self.deltateta < 181:
				self.mover.esqAx(self.deltateta)
			else:
				self.mover.dirAx(360-self.deltateta)
		elif self.deltay < 0 and self.deltax > 0:
			self.alpha = self.teta-self.ang
			self.deltateta = 360+self.ang-self.teta
			self.mover.dirAx(self.alpha)
		else:
			print "nenhuma condicao satisfeita"
		time.sleep(5)
		#deltateta eh o angulo positivo entre a orientacao do robo e a orientacao final
		
		self.d = distancia/10
		for i in range(int(self.d+1)):
			self.P = self.local.readLoc('locRobo.json')
			self.gama = self.deltateta+self.teta	#gama = angulo em graus positivo absoluto do pf
			self.mover.tras(10)
			self.seno = math.sin(math.radians(self.gama))
			self.cosseno = math.cos(math.radians(self.gama))
			self.deltay = self.seno*10 #deslocamento em y a cada 10mm percorridos
			self.deltax = self.cosseno*10 #deslocamento em x a cada 10mm percorridos
			self.xf = self.P[2]+self.deltax	#Px atual
			self.yf = self.P[3]+self.deltay	#Py atual
			self.local.writeLoc('locRobo.json',xf,yf,seno,cosseno,gama)
	
