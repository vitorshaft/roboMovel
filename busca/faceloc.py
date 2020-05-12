import numpy as np
import cv2

class loc:
	def __init__(self):
		self.cascata = cv2.CascadeClassifier('/home/pi/Imagem/haarcascade_frontalface_default.xml')
		self.cap = cv2.VideoCapture(1)
	def rastrear(self):
		self.existe, self.frame = self.cap.read()
		if(self.existe == False):
			self.cap.release()
			return
		self.cinza = cv2.cvtColor(self.frame,cv2.COLOR_BGR2GRAY)
		self.faces = self.cascata.detectMultiScale(self.cinza, 1.3, 5) #valores padrao
		#para cada face detectada
		for (x,y,w,h) in self.faces:
			self.centroX = x+(w/2)
			return [h,self.centroX]
