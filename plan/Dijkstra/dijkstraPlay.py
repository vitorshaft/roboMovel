import localizacao.pyAndar as andar
import plan.rota as rota
import localizacao.locRoboP3 as lugar
import time
import math
import argparse

ap = argparse.ArgumentParser(description= '(x,y) do objetivo')
ap.add_argument(	'objetivoX', type=int, help= 'entre com as coordenadas do objetivo separadas por espaco')
ap.add_argument(	'objetivoY', type=int, help= 'entre com as coordenadas do objetivo separadas por espaco')
args = ap.parse_args()
print(args.objetivoX,args.objetivoY)

x = andar.mover()
p = rota.plan()
coor = lugar.loc()

arquivoRobo = '/home/pi/roboMovel/locRobo.json'		#json com a localizacao do robo em formato [seno,cos,x,y,teta]
pRobo = coor.readLoc(arquivoRobo) #[seno,cos,x,y,teta]
xR = pRobo[2]
yR = pRobo[3]
teta = pRobo[4]
xis = args.objetivoX
ips = args.objetivoY
with open('caminho.json') as jsonFile:
	dados = json.load(jsonFile)
	inicioObj = '%d %d %d %d'%(xR,yR,xis,ips)
	caminho = dados[inicioObj]
	pontos = caminho[inicioObj]
#while(True):
for item in range(len(pontos)):
	pRobo = coor.readLoc(arquivoRobo) #[seno,cos,x,y,teta]
	xR = pRobo[2]
	yR = pRobo[3]
	teta = pRobo[4]
	xis = pontos[item][0]
	ips = pontos[item][1]
	
	""" INSERIR INTERACAO COM MOVIMENTO PARA CADA VALOR EM pontos"""
	dPolar = p.traj(xis,ips,xR,yR) #[angulo,dist]
	print ("virando para %d graus e andando %d cm"%(dPolar[0],dPolar[1]))
	print(dPolar[0]-teta)
	if (dPolar[0]-teta > 0):
		x.esqRad(dPolar[0]-teta)
	elif (dPolar[0]-teta < 0):
		x.dirRad((dPolar[0]-teta)*-1)
	x.parar()
	time.sleep(1)
	x.frente(dPolar[1])
	time.sleep(1)
	sen = math.sin(math.radians(dPolar[0]))
	cos = math.cos(math.radians(dPolar[0]))
	coor.writeLoc(arquivoRobo,xis,ips,sen,cos,dPolar[0]) #(arq,x,y,sen,cos,teta)
	time.sleep(1)
	s = input("Entre S para sair: ")
	if s == "s":
		break
