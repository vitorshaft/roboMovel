import RPi.GPIO as GPIO
import cv2
import numpy as np
import time
import laser
import localizacao.coordenadas as coord

ls = laser.laser()
conv = coord.converter()

servoPIN = 16
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(servoPIN, GPIO.OUT)
p = GPIO.PWM(servoPIN, 50)
p.start(0)

targets = {}

try:
	frame = np.ones((100,100,3), np.uint8)
	cv2.circle(frame,(50,50),2,(250,0,0),2)
	while True:
		for a in range(0,180,5):
			dist = int(ls.dLaser()/10)	#conversao para cm
			print(dist)
			
			if dist != -1 and dist <=50:
				item = conv.polarCart(a,dist)
				xis = int(item[2]+50)
				ips = int(item[3])
				print (xis, ips)
				cv2.circle(frame,(xis,ips),2,(0,0,250),1)
			
			
			a = 180 - a
			dc = int(1.0/18.0 * a + 2)
			p.ChangeDutyCycle(dc)
			time.sleep(0.01)
			cv2.imwrite('telaLIDAR.jpg',frame)
			imagem = cv2.imread('telaLIDAR.jpg',0)
			cv2.imshow('RMR2 - LIDAR', frame)
			time.sleep(1)
			'''if cv2.waitKey(0) == ord('q'):
				pass
			'''
		for a in range(180,0,-5):
			dist = int(ls.dLaser()/10)	#conversao para cm
			print(dist)
			
			if dist != -1 and dist <=50:
				item = conv.polarCart(a,dist)
				xis = int(item[2]+50)
				ips = int(item[3])
				print (xis, ips)
				cv2.circle(frame,(xis,ips),2,(0,0,250),1)
			
			a = 180 - a
			dc = int(1.0/18.0 * a +2)
			p.ChangeDutyCycle(dc)
			time.sleep(0.01)
			cv2.imwrite('telaLIDAR.jpg',frame)
			imagem = cv2.imread('telaLIDAR.jpg',0)
			cv2.imshow('RMR2 - LIDAR', imagem)
			time.sleep(1)
			'''if cv2.waitKey(0) == ord('q'):
				pass
			'''

except KeyboardInterrupt:
	print ('Servo desligado')
	p.stop()
	GPIO.cleanup()
	#cv2.destroyAllWindows()
except Exception as e:
	print (e)
	print ('Servo desligado')
	p.stop()
	GPIO.cleanup
	#cv2.destroyAllWindows()
	
