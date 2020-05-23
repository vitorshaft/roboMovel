import locRobo as LR
import math

l = LR.loc()
xis = int(input("Entre com X: "))
ips = int(input("Entre com Y: "))
ang = int(input("Entre com o angulo: "))
sen = math.sin(math.radians(ang))
cos = math.cos(math.radians(ang))
l.writeLoc('/home/pi/roboMovel/locRobo.json',xis,ips,sen,cos,ang)
print "Pi resetado para P(%d,%d,%d)"%(xis,ips,ang)
