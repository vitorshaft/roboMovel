#arrodeio
import math

class contorno:
	def __init__(self):
		self.todos = []
	def lerObs(self,arq):
		self.texto = open(arq, 'r')
		self.obs = self.texto.readline()
		self.obs = self.obs[:-1].split(',')
		for item in range(len(self.obs)):
			self.obs[item] = int(self.obs[item])
		return self.obs
	def pontosObs(self,lista,pRobo,pObj):	#lista[Xi,Yi,Xf,Yf],pRobo[sen,cos,x,y,teta],pObj[x,y]
		import numpy as np
		self.mapa = np.ones((lista[2]-lista[0],lista[3]-lista[1],2))
		for item in range(len(self.mapa)):
			for i in range(len(self.mapa[item])):
				self.mapa[item][i] = [i+lista[1],item+lista[0]]
		import rota
		p = rota.plan()
		self.eq = p.traj(pObj[0],pObj[1],pRobo[2],pRobo[3])
		self.a = math.tan(math.radians(self.eq[0]))
		self.b = pObj[1]-(self.a*pObj[0])
		self.secante = []
		for x in range(len(self.mapa)):
			for y in range(len(self.mapa[item])):
				if (y == (self.a*x)+self.b):
					self.secante.append(mapa[x][y])	#conjunto de pontos do obs que interceptam a rota
		return self.secante
					
