import localizacao.pyAndar as andar
import plan.rota as rota
import localizacao.locRoboP3 as lugar
import time
import math

x = andar.mover()
p = rota.plan()
coor = lugar.loc()

arquivoRobo = '/home/pi/roboMovel/locRobo.json'
listaX = [-20.0,0.0]
listaY = [20.0,0.0]
while(True):
#for item in range(2):
	pRobo = coor.readLoc(arquivoRobo) #[seno,cos,x,y,teta]
	xR = pRobo[2]
	yR = pRobo[3]
	teta = pRobo[4]
	xis = float(input("Entre com o X do obj: "))
	ips = float(input("Entre com o Y do obj: "))
	#xis = listaX[item]
	#ips = listaY[item]
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
	
