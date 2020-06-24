#import os
import laser
import busca.buscarObj
import localizacao.locRoboP3
import localizacao.pyAndar as andar
import localizacao.coordenadas
from time import sleep

''' SEQUENCIA DE MAPEAMENTO:
1. Girar 180 para direita e 180 para esquerda
2. Seguir em frente caso não esteja obstruido
3. Armazenar distancias menores que 1000 mm
3.1 Salvar posicao do robo (x,y,alfa) e distancia 
4. Converte pos/dist em posicao cartesiana de obs
5. Salva posicoes em arquivo txt separadas por linha e agrupadas em listas

Mindstorm:
- Checar obstáculo a frente: if(dist obstáculo < 1000): parar, andar dist, virar 90 graus, repete
'''
#objetos
ls = laser.laser()
bs = busca.buscarObj.buscar()
loc = localizacao.locRoboP3.loc()
mv = andar.mover()
cv = localizacao.coordenadas.converter()

#arquivos e BD
arqRobo = '/home/pi//roboMovel/locRobo.json'
amb = '/home/pi/roboMovel/ambiente.txt'
fixos = '/home/pi/roboMovel/fixos.txt'

#girar 180 dir/esq
'''
mv.dirAx(180)
sleep(1)
mv.esqAx(180)
sleep(1)
'''
#caso não tenha obs em 100 mm, seguir em frente até detectar obs

def seguir():
	if ls.dLaser() > 100:
		d = mv.frenteLendo(60)	#armazena distancia andada enquanto frenteLendo(%PWM)
	else:
		mv.frenteLendo(0)
	return (d)

def mapear ():
	pRobo = loc.readLoc(arqRobo)	#le a pos do robo
	dObs = ls.dLaser()	#mede a distancia
	relObs = cv.polarCart(pRobo[4],dObs)	#posicao do obs relativa ao robo
	absObs = [int(pRobo[2]+relObs[2]),int(pRobo[3]+relObs[3])]	#posicao do obs absoluta
	guardar = open(amb,'a')	#abre arquivo txt de obstaculos
	guardar.write(str(absObs)+'\n')	#salva ponto detectado
	print(dObs,relObs,absObs)	#printa distancia, pos relativa e pos absoluta do obstaculo
	

#- Checar obstáculo a frente: if(dist obstáculo < 1000): parar, andar dist, virar 90 graus, repete

def slam():	#para ser usada com while

	inicialR = loc.readLoc(arqRobo)	#[sen,cos,x,y,teta]
	dObs = ls.dLaser()/10	#mede distancia ate obs, converte em cm
	if (dObs < 80):	#caso detecte alguma coisa em menos de 1 m
		mv.parar()	#para
		print("andando ate o obstaculo")
		sleep(1)	#espera 1s
		mv.frente(dObs - 15)	#anda ate 15 cm do obstaculo
		print("escaneando 180 pela Esq")
		sleep(1)	#espera mais 1s
		mv.parar()	#para novamente
		'''	MAPEAMENTO	'''
		ang = inicialR[4]
		for a in range(12):	# Faz 12 medicoes de distancia
			print(ang)
			mv.esqRad(15)	# vira 15 graus a esquerda
			sleep(0.5)	# espera 0,5s
			ang = ang+15	# atualiza angulo absoluto do Robo
			if ang > 360:
				ang = ang-360	#reseta rotacao caso passe de 360
			#print (ang)
			relObs = cv.polarCart(ang,dObs)	# gera posicao relativa do obs ao Robo
			absObs = [int(inicialR[2]+relObs[2]),int(inicialR[3]+relObs[3])]	#posicao do obs absoluta
			guardar = open(amb,'a')	#abre arquivo txt de obstaculos. a = append, w = sobrescrever, r = read
			guardar.write(str(absObs)+'\n')	#salva ponto detectado
			guardar.close()	#salva e fecha o arquivo txt
			print("seguindo pela esq")
			sleep(1)
			mv.dirRad(90)
			ang = ang-90
			if ang < 0:
				ang = 360+ang
		atualR = dObs-15	#atualiza distancia percorrida
	else:	#caso nao detecte obs em 1 metro
		print("nada detectado")
		sleep(1)
		mv.frenteLendo(70)		#guarda distancia percorrida
		atualR = max(mv.pEsq,mv.pDir)*30
		ang = inicialR[4]	#angulo (permanece)
	finalR = cv.polarCart(ang,atualR)	# converte polar em cartesiano(angulo, distancia). Retorna [sen,cos,x,y]
		
	xR = inicialR[2]+finalR[2]	#transformada de X do Robo
	yR = inicialR[3]+finalR[3]	#transformada de Y do Robo
	sR = finalR[0]	#seno
	cR = finalR[1]	#cosseno
	
	loc.writeLoc(arqRobo,xR,yR,sR,cR,ang)
	fixo = open(fixos,'a')
	fixo.write(str(int(xR))+','+str(int(yR))+'\n')
	fixo.close()
	mv.parar()
	
#OLHAR MAPA.JPG ANTES DE CONTINUAR
#os.system("python3 monitorCam.py")
for item in range(4):
	slam()
'''
for i in range(9):
	mapear()
	pR = loc.readLoc(arqRobo) #[sen,cos,x,y,teta]
	mv.dirRad(10)
	loc.writeLoc(arqRobo,pR[2],pR[3],pR[0],pR[1],pR[4]-10)
'''
