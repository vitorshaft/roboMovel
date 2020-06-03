import math

class plan:
	def __init__(self):
		pass
	def traj(self,xo,yo,xr,yr):
		self.dx = float(xo-xr)
		self.dy = float(yo-yr)
		try:
			self.tg = self.dy/self.dx
		except:
			self.tg = self.dy/(self.dx+0.0000000000001)
		self.h = math.hypot(self.dx,self.dy)
		self.teta = math.atan(self.tg)
		self.seno = self.dy/self.h
		self.cos = self.dx/self.h
		if (self.seno > 0 and self.cos > 0):	#Q1
			self.alfa = math.degrees(math.atan(self.tg))
		elif (self.seno > 0 and self.cos < 0):	#Q2
			self.alfa = math.degrees(math.acos(self.cos))
		elif (self.seno < 0 and self.cos <0):	#Q3
			self.alfa = math.degrees(math.atan(self.tg))+180
		elif (self.seno < 0 and self.cos >0):	#Q4
			self.alfa = math.degrees(math.atan(self.tg))+360
		elif (self.seno == 0 and self.cos > 0):
			self.alfa = 0.0
		elif (self.seno == 0 and self.cos < 0):
			self.alfa = 180.0
		elif (self.seno > 0 and self.cos == 0):
			self.alfa = 90.0
		elif (self.seno < 0 and self.cos == 0):
			self.alfa = 270.0
		else:
			print("CONDICAO TRIGONOMETRICA NAO ATENDIDA")
		
		#print(self.alfa,self.h)
		return [self.alfa,self.h]
