'''BUSCA OBJETIVO (ROSTO) E SE APROXIMA'''

import cv2
from time import sleep
import localizacao.pyAndar as andar
#import busca.recog
import busca.faceloc as face
import localizacao.locRoboP3 as lugar
import localizacao.coordenadas as coord

#distancia entre rodas = 115 mm. Ao centro = 57,5 mm
#diametro roda = 38 mm

#ident = busca.recog.identificar()
ident = face.loc()
x = andar.mover()
coor = lugar.loc()
conv = coord.converter()	#polarCart(teta,dist)>[sen,cos,x,y] cartPolar(x,y)>[teta,dist]
arquivoRobo = '/home/pi/roboMovel/locRobo.json'
arquivoObj = '/home/pi/roboMovel/locObj.json'
passo = 0
achei = 0

while(True):
	#global passo
	#f = open("angular.txt","r")
	#posicao = ident.comparar()
	pRobo = coor.readLoc(arquivoRobo) #[seno,cos,x,y,teta]
	passo = pRobo[4]
	posicao = ident.rastrear()
	sleep(0.5)
	if posicao == None:
		print("buscando objetivo")
		if passo >= 360:
			passo = passo-360	#se passo = 355, passo+15 = 370 -> corrigir
		
		x.esqRad(15)
		passo = passo+15 #posicao angular absoluta
		#o centro eh deslocado quando a rotacao eh radial. Eh necessario encontrar os X e Y do centro com conv.polarCart()
		centro = conv.polarCart(passo,58)
		'''os valores do centro sao relativos, no JSON da posicao do robo os valores sao absolutos
		por isso os valores relativos sao somados aos anteriores para virarem absolutos'''
		coor.writeLoc(arquivoRobo,centro[0],centro[1],pRobo[2]+centro[2],pRobo[3]+centro[3],passo)
		sleep(1)
	elif posicao[0] < 200:
		h = posicao[0]
		
		print("indo ao objetivo",h)
		
		sleep(1)
		if achei == 0:
			x.dirRad(30)
			sleep(0.5)
			x.dirRad(30)
			sleep(1)
			achei = 1
		#else:
		x.frente(30)
		desloc = conv.polarCart(passo,30)
		coor.writeLoc(arquivoRobo,pRobo[2]+desloc[2],pRobo[3]+desloc[3],desloc[0],desloc[1],passo)
		dObj = (775*230)/h
		pObj = conv.polarCart(passo,dObj) #calcula a posicao do obj em relacao ao robo. Passo = angulo do robo, dObj = hipotenusa
		import busca.locObjP3
		obj = busca.locObjP3.locobj()
		#ant = obj.readObj('/home/pi/roboMovel/locObj.json')
		obj.writeObj(arquivoObj,pRobo[2]+pObj[2],pRobo[3]+pObj[3]) #computa localizacao do obj em relacao ao ambiente
		print("objeto avistado a %d cm"%dObj)
		sleep(1)
		x.parar()
		break
		
	elif posicao[0] >= 200:
		h = posicao[0]
		print("objetivo atingido",h)
		#escrever algoritmo de posicao do objetivo
		dObj = (775*230)/h
		pObj = conv.polarCart(passo,dObj)
		import busca.locObjP3
		obj = busca.locObjP3.locobj()
		#ant = obj.readObj('/home/pi/roboMovel/locObj.json')
		obj.writeObj(arquivoObj,pRobo[2]+pObj[2],pRobo[3]+pObj[3]) #computa localizacao do obj em relacao ao ambiente
		print("objeto avistado a %d cm"%dObj)
		sleep(1)
		x.parar()
		break
	else:
		print(posicao)
	
	if(cv2.waitKey(200) & 0xFF == ord('q')):		#artificio para interromper exibicao da webcam apenas com a tecla 'q'
		break
#ident.video_capture.release()
ident.cap.release()
cv2.destroyAllWindows()
