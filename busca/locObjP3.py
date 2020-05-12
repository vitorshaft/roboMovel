import os
import json

#MODULO DE CONTROLE DO BD DE POSICAO DE OBJETOS

class locobj:
	def __init__(self):
		self.dados = {}
		self.dados['loc'] = [0]
	def readObj(self,arq):
		with open(arq) as jsonFile:
			data = json.load(jsonFile)
			self.DB = data['loc']
			
			self.x = self.DB[0]['px']
			self.y = self.DB[0]['py']
			
			return [self.x,self.y]

	def writeObj(self,arq,x,y):
		self.dados['loc'][0] = {"px": x, "py": y}
		print (self.dados['loc'][0])
		with open(arq,'w') as BD:
			json.dump(self.dados,BD)
