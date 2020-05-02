import cv2
from time import sleep
import pyAndar as andar
import busca.recog

ident = busca.recog.identificar()
x = andar.mover()
passo = 0
achei = 0

while(True):
	posicao = ident.comparar()
	sleep(0.5)
	if posicao == None:
		print("buscando objetivo")
		#if ser.read(1) == b'a':	#1 eh o tamanho de bytes a serem lidos
		x.esqRad(15)
		sleep(1)
	elif posicao[0] < 320:
		h = posicao[0]
		#c = posicao[1]
		print("indo ao objetivo",h)
		
		time.sleep(1)
		x.frente(5)
		
	elif posicao[0] >= 320:
		h = posicao[0]
		print("objetivo atingido",h)
		time.sleep(1)
		x.parar()
		break
	else:
		print(posicao)
	
	if(cv2.waitKey(200) & 0xFF == ord('q')):		#artificio para interromper exibicao da webcam apenas com a tecla 'q'
		break
ident.video_capture.release()
cv2.destroyAllWindows()
