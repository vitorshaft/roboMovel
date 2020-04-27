import cv2
import time
import serial
ser = serial.Serial("/dev/ttyUSB0",9600)	#USB
#ser = serial.Serial("/dev/ttyS0",9600,timeout=1)	#UART

import busca.recog

ident = busca.recog.identificar()
passo = 0
achei = 0

while(True):
	posicao = ident.comparar()
	'''
	rec = ser.readline()
	print(rec)
	if rec == b'a':
		passo+=1
		pass
	else:
		pass
	'''
	time.sleep(0.5)
	if posicao == None:
		print("buscando objetivo")
		#if ser.read(1) == b'a':	#1 eh o tamanho de bytes a serem lidos
		ser.write(b'2')
		rec = ser.readline()
		print(rec)
		if rec == b'a50\r\n':
			passo+=1
			print("passos: ",passo)
			pass
		else:
			print("passos: ",passo)
			pass
	elif posicao[0] < 320:
		ser.write(b'9')
		h = posicao[0]
		#c = posicao[1]
		print("indo ao objetivo",h)
		#if ser.read() == b'a':
		'''
		if c < 140:
			ser.write(b'3')
		elif c > 290:
			ser.write(b'2')
		'''
		achei = passo
		time.sleep(1)
		'''
		if passo > achei:
			for giro in range(passo-achei):
				ser.write(b'3')
		'''
		for g in range(5):
			ser.write(b'3')
			time.sleep(1)
		ser.write(b'0')
		
	elif posicao[0] >= 320:
		ser.write(b'9')
		h = posicao[0]
		print("objetivo atingido",h)
		achei = passo
		time.sleep(1)
		'''
		if passo > achei:
			for g in range(passo-achei):
				ser.write(b'3')
		'''
		for g in range(3):
			ser.write(b'3')
		break
	else:
		print(posicao)
	
	if(cv2.waitKey(200) & 0xFF == ord('q')):		#artificio para interromper exibicao da webcam apenas com a tecla 'q'
		break
ident.video_capture.release()
cv2.destroyAllWindows()
