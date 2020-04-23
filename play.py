import cv2
import time

import localizacao.stepper
import busca.buscarObj
import busca.recog


#procurar = busca.buscarObj.buscar()
desloc = localizacao.stepper.andar()
ident = busca.recog.identificar()
b = 10
while(True):
	h = ident.comparar()
	time.sleep(1)
	if h == None:
		print("buscando objetivo",h)
		#procurar.procura('quad')
		desloc.frente(b)
		desloc.esqAx(90)
		b = b+10
		time.sleep(1)
	elif h < 300:
		print("indo ao objetivo",h)
		#D = 14400/h
		desloc.frente(5)	#anda 5 cm na direcao do objetivo
		
	elif h > 300:
		print("objetivo atingido",h)
	else:
		print(h)
	
	if(cv2.waitKey(200) & 0xFF == ord('q')):		#artificio para interromper exibicao da webcam apenas com a tecla 'q'
		break
ident.video_capture.release()
cv2.destroyAllWindows()
