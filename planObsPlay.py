import localizacao.pyAndar as andar
import plan.rota as rota
import localizacao.locRoboP3 as lugar
import plan.desvio
import time
import math

x = andar.mover()
p = rota.plan()
coor = lugar.loc()
cont = plan.desvio.contorno()

arquivoRobo = '/home/pi/roboMovel/locRobo.json'
pRobo = coor.readLoc(arquivoRobo) #[seno,cos,x,y,teta] #posicao inicial do Robo
xis = float(input("Entre com o X do obj: "))
ips = float(input("Entre com o Y do obj: "))
#pObj = [xis,ips]	#posicao do objetivo
pObj = [ips,xis]
obstac = '/home/pi/roboMovel/plan/obs.txt'
obs = cont.lerObs(obstac)
intersec = cont.pontosObs(obs,pRobo,pObj)	#lista[Xi,Yi,Xf,Yf],pRobo[sen,cos,x,y,teta],pObj[x,y]
print (intersec)
h = []
for i in intersec:
	hip = math.hypot(i[0],i[1])
	h.append(hip)
#di = min(h) #distancia de interseccao mais proximo
#df = max(h) #distancia de interseccao mais distante
try:
	pi = intersec[h.index(min(h))]
	pf = intersec[h.index(max(h))]
except:
	pi = [pRobo[2],pRobo[3]] #caso a rota nao intercepte o obstaculo
	pf = [pObj[0],pObj[1]] #pi e a posicao do robo e pf a do objetivo
	obs = [pRobo[2],pRobo[3],pObj[0],pObj[1]]
	
if (pi[0] < pi[1]):
	roteiro = [pi,[obs[0],obs[3]],pf,[xis,ips]]	#arrodeia pelo lado mais curto
else:
	roteiro = [pi,[obs[2],obs[1]],pf,[xis,ips]]
	
#while(True):
for item in range(len(roteiro)):
	pRobo = coor.readLoc(arquivoRobo) #[seno,cos,x,y,teta]	#posicao atual do Robo
	xR = pRobo[2]
	yR = pRobo[3]
	teta = pRobo[4]
	#xis = float(input("Entre com o X do obj: "))
	#ips = float(input("Entre com o Y do obj: "))
	xis = roteiro[item][0]
	ips = roteiro[item][1]
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

