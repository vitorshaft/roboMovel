import cv2
from time import sleep
import pyAndar as andar
import busca.recog

ident = busca.recog.identificar()
x = andar.mover()
passo = 0
achei = 0

while(True):
	#global passo
	#f = open("angular.txt","r")
	posicao = ident.comparar()
	sleep(0.5)
	if posicao == None:
		print("buscando objetivo")
		passo = passo+15
		f = open("angular.txt","w")	
		x.esqRad(15)
		f.write("%d"%passo)
		f.close()
		sleep(1)
	elif posicao[0] < 320:
		h = posicao[0]
		#c = posicao[1]
		r = open("angular.txt","r")
		
		print("indo ao objetivo",h)
		
		sleep(1)
		if achei == 0:
			x.dirRad(15)
			sleep(0.5)
			x.dirRad(15)
			sleep(1)
			achei = 1
		#else:
		x.frente(5)
		
	elif posicao[0] >= 320:
		h = posicao[0]
		print("objetivo atingido",h)
		sleep(1)
		x.parar()
		break
	else:
		print(posicao)
	
	if(cv2.waitKey(200) & 0xFF == ord('q')):		#artificio para interromper exibicao da webcam apenas com a tecla 'q'
		break
ident.video_capture.release()
cv2.destroyAllWindows()
