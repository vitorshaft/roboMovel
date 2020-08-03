import RPi.GPIO as GPIO
import time
import laser
import json

ls = laser.laser()

servoPIN = 16
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(servoPIN, GPIO.OUT)
p = GPIO.PWM(servoPIN, 50)
p.start(0)

targets = {}

try:
	#mapa = open('lidar.txt','a')
	targets['loc'] = [0]
	for a in range(0,180):
		dist = int(ls.dLaser()/10)	#conversao para cm
		print(dist)
			
		if dist != -1 and dist <=50:
			targets['loc'][0] = {a:dist}
			with open('lidar.json','w') as BD:
				json.dump(targets,BD)
			
		else:
			targets['loc'][0] = {a:50}
			with open('lidar.json','w') as BD:
				json.dump(targets,BD)
			
			
			a = 180 - a
			dc = int(1.0/18.0 * a + 2)
			p.ChangeDutyCycle(dc)
			time.sleep(0.01)

	for a in range(180,0,-1):
		dist = int(ls.dLaser()/10)	#conversao para cm
		print(dist)
			
			
		if dist != -1 and dist <=50:
			targets['loc'][0] = {a:dist}
			with open('lidar.json','w') as BD:
				json.dump(targets,BD)
			
		else:
			targets['loc'][0] = {a:50}
			with open('lidar.json','w') as BD:
				json.dump(targets,BD)
			
			a = 180 - a
			dc = int(1.0/18.0 * a +2)
			p.ChangeDutyCycle(dc)
			time.sleep(0.01)
	
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
