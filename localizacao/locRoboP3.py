import os
import json

#LIB QUE RETORNA DADOS DA LOCALIZACAO DO ROBO

class loc:
	def __init__(self):
		self.dados = {}
		self.dados['loc'] = [0]
	def readLoc(self,arq):
		with open(arq) as jsonFile:
			data = json.load(jsonFile)
			self.DB = data['loc']
			self.seno = self.DB[0]['sen']
			self.cosseno = self.DB[0]['cos']
			self.x = self.DB[0]['px']
			self.y = self.DB[0]['py']
			self.teta = self.DB[0]['teta']
			return [self.seno,self.cosseno,self.x,self.y,self.teta]

	def writeLoc(self,arq,x,y,sen,cos,teta):
		self.dados['loc'][0] = {"sen": sen, "cos": cos, "px": x, "py": y, "teta": teta}
		print (self.dados['loc'][0])
		with open(arq,'w') as BD:
			json.dump(self.dados,BD)
