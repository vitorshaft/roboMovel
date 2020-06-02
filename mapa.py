import cv2
import numpy as np
import plan.desvio
import localizacao.locRoboP3 as lugar

arquivoRobo = '/home/pi/roboMovel/locRobo.json'
coor = lugar.loc()
cont = plan.desvio.contorno()
pR = coor.readLoc(arquivoRobo)
obs = cont.lerObs('/home/pi/roboMovel/plan/obs.txt')

foto = np.ones((300,400,3), np.uint8)

cv2.circle(foto,(int(pR[2]),int(pR[3])),16,(204,204,0),2) #robo em azul
cv2.rectangle(foto,(obs[0], obs[1]),(obs[2],obs[3]),(200,200,200),2) #obstaculo em cinza claro
cv2.line(foto,(0,0),(27,20),(0,0,250),2)
cv2.line(foto,(27,20),(40,20),(0,0,250),2)
cv2.line(foto,(40,20),(39,29),(0,0,250),2)
cv2.line(foto,(39,29),(60,80),(0,0,250),2)
'''
cv2.line(foto,(500,1366),(1500,1366),(130,130,130),20)
cv2.line(foto,(1500,1366),(1000,500),(130,130,130),20)
cv2.line(foto,(1000,500),(500,1366),(130,130,130),20)
'''
cv2.imwrite("mapa.jpg",foto)
