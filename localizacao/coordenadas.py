import math

class converter:
	def __init__(self):
		pass
	def polarCart(self,ang,d):	#converte coord polar (angulo, distancia) em cartesiana (x,y)
		self.alfa = math.radians(ang)
		self.seno = math.sin(self.alfa)
		self.cos = math.cos(self.alfa)
		self.x = math.cos(self.alfa)*d
		self.y = math.sin(self.alfa)*d
		return [self.seno,self.cos,self.x,self.y]
	def cartPolar(self,x,y):
		self.hip = math.hypot(x,y)
		self.seno = y/self.hip
		self.teta = math.degrees(math.asin(self.seno))
		return [self.teta,self.hip]
