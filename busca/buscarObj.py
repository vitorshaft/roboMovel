#usar python3
import busca.recog
import localizacao.stepper
import time
import localizacao.locRoboP3
import localizacao.deslocarP3
import busca.locObjP3

class buscar:
	def __init__(self):
		self.plotar = busca.locObjP3.locobj()
		pass
		
	def procura(self,padrao):
		self.mexer = localizacao.stepper.andar()
		if padrao == 'quad':
			#self.a = True
			while True:
				b = 100
				self.mexer.frente(b)
				self.mexer.esqAx(90)
				b = b+100
				time.sleep(1)
				
	def posObj(self,D):
		#calcula posicao do objeto em funcao da distancia e do angulo do robo ao identifica-lo
		self.posicao = localizacao.locRoboP3.loc()
		self.atual = self.posicao.readLoc('locRobo.json')
		self.seno = self.atual[0]
		self.cosseno = self.atual[1]
		self.xR = self.atual[2]
		self.yR = self.atual[3]
		self.xO = (D*self.cosseno)+self.xR #X do obj
		self.yO = (D*self.seno)+self.yR #Y do Obj
		self.plotar.writeObj('locObj.json',self.xO,self.yO)
		return [self.xO,self.yO]
		
