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

#girar 180 dir/esq
'''
mv.dirAx(180)
sleep(1)
mv.esqAx(180)
sleep(1)
'''
#caso não tenha obs em 100 mm, seguir em frente até detectar obs
'''
def seguir():
	if ls.dLaser() > 100:
		d = mv.frenteLendo(60)	#armazena distancia andada enquanto frenteLendo(%PWM)
	else:
		mv.frenteLendo(0)
	return (d)
'''
def mapear ():
	pRobo = loc.readLoc(arqRobo)	#le a pos do robo
	dObs = ls.dLaser()	#mede a distancia
	relObs = cv.polarCart(pRobo[4],dObs)	#posicao do obs relativa ao robo
	absObs = [int(pRobo[2]+relObs[2]),int(pRobo[3]+relObs[3])]	#posicao do obs absoluta
	guardar = open(amb,'a')	#abre arquivo txt de obstaculos
	guardar.write(str(absObs)+'\n')	#salva ponto detectado
	print(dObs,relObs,absObs)	#printa distancia e pos absoluta do obstaculo
	
'''
def slam():
	inicialR = loc.readLoc(arqRobo)	#[sen,cos,x,y,teta]
	finalR = cv.polarCart(inicialR[4],seguir())	#[sen,cos,x,y]
	xR = inicialR[2]+finalR[2]
	yR = inicialR[3]+finalR[3]
	sR = finalR[0]
	cR = finalR[1]
	tetaR = inicialR[4]
	
	dObs = ls.dLaser()
	loc.writeLoc(arqRobo,xR,yR,sR,cR,tetaR)
'''
for i in range(9):
	mapear()
	pR = loc.readLoc(arqRobo) #[sen,cos,x,y,teta]
	mv.dirRad(10)
	loc.writeLoc(arqRobo,pR[2],pR[3],pR[0],pR[1],pR[4]-10)
