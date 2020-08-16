import cv2
import numpy as np

largura = 270
altura = 270

mapa = np.zeros((largura,altura),np.uint8)
def plotarObs(x,y,X,Y):
	for linha in range(largura):
		for col in range(altura):
			if linha >= y and linha <= Y:
				if col >= x and col <= X:
					mapa.itemset((linha,col),255)
plotarObs(60,0,220,90)
plotarObs(0,180,160,270)
plotarObs(180,180,265,265)
cv2.imwrite("mapa.jpg",mapa)
