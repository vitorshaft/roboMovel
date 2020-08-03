import RPi.GPIO as GPIO
import pygame
import math
import time
import colors
import sys
import cv2
from target import *
from display import draw
import laser

print('Iniciando RADAR')

x = pygame.init()
pygame.font.init()
defaultFont = pygame.font.get_default_font()
fontRenderer = pygame.font.Font(defaultFont, 20)
radarDisplay = pygame.display.set_mode((1400, 800))
pygame.display.set_caption('Tela do RADAR')

ls = laser.laser()

servoPIN = 16
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(servoPIN, GPIO.OUT)
p = GPIO.PWM(servoPIN, 50)
p.start(0)

targets = {}

try:
	while True:
		
		for a in range(0,180):
			dist = int(ls.dLaser()/10)	#conversao para cm
			print(dist)
			
			if dist != -1 and dist <=50:
				targets[a] = Target(a,dist)
			else:
				targets[a] = Target(a,50)
			draw(radarDisplay,targets,a,dist,fontRenderer)
			
			a = 180 - a
			dc = 1.0/18.0 * a + 2
			p.ChangeDutyCycle(dc)
			time.sleep(0.001)
			
		for a in range(180,0,-1):
			dist = int(ls.dLaser()/10)	#conversao para cm
			print(dist)
			
			if dist != -1 and dist <=50:
				targets[a] = Target(a,dist)
			else:
				targets[a] = Target(a,50)
			draw(radarDisplay,targets,a,dist,fontRenderer)
			
			a = 180 - a
			dc = 1.0/18.0 * a +2
			p.ChangeDutyCycle(dc)
			time.sleep(0.001)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				raise KeyboardInterrupt

except KeyboardInterrupt:
	print ('Servo desligado')
	p.stop()
	GPIO.cleanup()
except Exception as e:
	print (e)
	print ('Servo desligado')
	p.stop()
	GPIO.cleanup()
	
