import math

class plan:
	def __init__(self):
		pass
	def traj(self,xo,yo,xr,yr):
		self.a = float(yo-yr)/float(xo-xr)
		self.teta = math.atan(self.a)
		self.alfa = math.degrees(self.teta)
		if (xo < 0 and yo > 0):
			self.alfa = self.alfa+180
		elif (xo < 0 and yo < 0):
			self.alfa = self.alfa+180
		elif (xo > 0 and yo < 0):
			self.alfa = self.alfa+ 360
		#self.b = yr -(self.a*xr)
		self.h = math.hypot((yo-yr),(xo-xr))
		return [self.alfa,self.h]
