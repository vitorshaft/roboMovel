import math
import time
import stepper
import locRobo

# SCRIPT PARA MOVIMENTAR O ROBO DO PI AO PF

local = locRobo.loc()

mover = stepper.andar()
#for i in range(1000):
def rastrear(d,ang):	#desloca o robo em d na direcao ang (graus)
	ler = local.readLoc('locRobo.json')
	dd = d/10
	mover.dirAx(ang)
	deltaang = ler[4]+ang
	time.sleep(5)
	for i in range(int(dd+1)):
		mover.tras(10)
		P = local.readLoc('locRobo.json')
		deltay = math.sin(math.radians(ang))*10
		deltax = math.cos(math.radians(ang))*10
		seno = math.sin(math.radians(ang))
		cosseno = math.cos(math.radians(ang))
		xf = P[2]+deltax
		yf = P[3]+deltay
		
		local.writeLoc('locRobo.json',xf,yf,seno,cosseno,deltaang)

def pipf(x,y):	#desloca o robo ate o ponto (x,y)
	P = local.readLoc('locRobo.json')
	s = P[0]
	c = P[1]
	deltax = x-P[2]
	deltay = y-P[3]
	teta = P[4]
	distancia = math.hypot(deltax,deltay)
	tg = deltay/deltax
	beta = math.atan(tg)
	ang = math.degrees(beta)
	
	
	if deltay > 0 and deltax > 0:
		deltateta = ang-teta
		mover.esqAx(deltateta)
	elif deltay > 0 and deltax < 0:
		deltateta = ang*(-1)+90-teta
		mover.esqAx(deltateta)
	elif deltay < 0 and deltax < 0:
		deltateta = ang+180-teta
		if deltateta < 181:
			mover.esqAx(deltateta)
		else:
			mover.dirAx(360-deltateta)
	elif deltay < 0 and deltax > 0:
		alpha = teta-ang
		deltateta = 360+ang-teta
		mover.dirAx(alpha)
	else:
		print "nenhuma condicao satisfeita"
	time.sleep(5)
	#deltateta eh o angulo positivo entre a orientacao do robo e a orientacao final
	
	d = distancia/10
	for i in range(int(d+1)):
		P = local.readLoc('locRobo.json')
		gama = deltateta+teta	#gama = angulo em graus positivo absoluto do pf
		mover.tras(10)
		seno = math.sin(math.radians(gama))
		cosseno = math.cos(math.radians(gama))
		deltay = seno*10 #deslocamento em y a cada 10mm percorridos
		deltax = cosseno*10 #deslocamento em x a cada 10mm percorridos
		xf = P[2]+deltax	#Px atual
		yf = P[3]+deltay	#Py atual
		local.writeLoc('locRobo.json',xf,yf,seno,cosseno,gama)

pipf(300,300)
time.sleep(1.5)
pipf(400,100)
time.sleep(1.5)
pipf(500,400)
'''
rastrear(1000,60)
'''
