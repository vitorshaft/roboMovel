import cv2
import numpy as np
import localizacao.locRoboP3

loc = localizacao.locRoboP3.loc()
cap = cv2.VideoCapture(1)
#if cap.isOpened():
while True:
	lerLaser = open('/home/pi/roboMovel/laserTopic.txt','r')
	dist = "distancia: "+lerLaser.read()+" cm"
	xyteta = loc.readLoc('/home/pi//roboMovel/locRobo.json')
	
	xis = "X: "+str(int(xyteta[2]))
	ips = "Y: "+str(int(xyteta[3]))
	teta = "ang: "+str(xyteta[4])+" graus"
	posicao = "posicao:"
	if cap.isOpened():	
		ret, frame = cap.read()
		cv2.circle(frame,(320,370),20,(0,250,0),2)
		cv2.line(frame,(320,20),(320,220),(0,250,0),1)
		cv2.line(frame,(20,240),(290,240),(0,250,0),1)
		cv2.line(frame,(320,260),(320,460),(0,250,0),1)
		cv2.line(frame,(350,240),(620,240),(0,250,0),1)
		
		cv2.putText(frame,posicao, (10,350),cv2.FONT_HERSHEY_SIMPLEX, 1, (0,250,0),2)
		cv2.putText(frame,xis, (10,400),cv2.FONT_HERSHEY_SIMPLEX, 1, (0,250,0),2)
		cv2.putText(frame,ips, (10,430),cv2.FONT_HERSHEY_SIMPLEX, 1, (0,250,0),2)
		cv2.putText(frame,teta, (10,460),cv2.FONT_HERSHEY_SIMPLEX, 1, (0,250,0),2)
		cv2.putText(frame,dist,(350,380),cv2.FONT_HERSHEY_PLAIN, 1, (255,255,255),1)
		cv2.imshow('RMR2 - Visao Primeira Pessoa', frame)
		if (cv2.waitKey(1) & 0xFF == ord('q')):
			break
	else:
		cap.open(1)
	

# Release handle to the webcam
cap.release()
cv2.destroyAllWindows()
