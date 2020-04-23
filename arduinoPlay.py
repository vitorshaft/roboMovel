import cv2
import time
import serial
#ser = serial.Serial("/dev/ttyUSB0",9600)	#USB
ser = serial.Serial("/dev/ttyS0",9600)	#UART

import busca.recog

ident = busca.recog.identificar()
b = 0
parada = str(chr(115))


while(True):
	posicao = ident.comparar()
	
	time.sleep(1.5)
	if posicao == None:
		print("buscando objetivo")
		#if ser.read(1) == 'a':	#1 eh o tamanho de bytes a serem lidos
		if b < 5:
			ser.write(b'2')
		elif b > 5 and b < 10:
			ser.write(b'3')
		else:
			b = 0
		b+=1

	elif posicao[0] < 280:
		ser.write(b'9')
		h = posicao[0]
		c = posicao[1]
		print("indo ao objetivo",h)
		#if ser.read() == 'a':
		if c < 140:
			ser.write(b'3')
		elif c > 290:
			ser.write(b'2')
		ser.write(b'0')
		
	elif posicao[0] >= 280:
		ser.write(b'9')
		h = posicao[0]
		print("objetivo atingido",h)
		break
	else:
		print(posicao)
	
	if(cv2.waitKey(200) & 0xFF == ord('q')):		#artificio para interromper exibicao da webcam apenas com a tecla 'q'
		break
ident.video_capture.release()
cv2.destroyAllWindows()
