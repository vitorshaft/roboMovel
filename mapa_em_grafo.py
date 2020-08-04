import cv2
import numpy as np
import math

jpg = 'mapa.jpg'
tamRobo = 30
entrada = input('insira os pontos de inicio e obj separados por espaço: ')
pts = entrada.split(' ')
inicio = [int(pts[0]),int(pts[1])]
obj = [int(pts[2]),int(pts[3])]

nome = 'grafo_'+pts[0]+'_'+pts[1]+'_a'+pts[2]+'_'+pts[3]
nomeB = 'bordas_'+pts[0]+'_'+pts[1]+'_a'+pts[2]+'_'+pts[3]

def vertices(inicio,imagem,obj):
	#parametros de deteccao de borda:
	inf = 0 
	sup = 255
	ker = 5
	#arquivo de imagem do mapa
	img = cv2.imread(imagem)
	#matriz imagem apenas com bordas dos obs detectados:
	bordas = cv2.Canny(img,inf,sup,ker)
	#lista para conter pontos das bordas
	pontos = []
	lados = np.where(bordas == 255)	#coleta coordenadas dos pixels das bordas
	#coordenadas iniciais e finais dos obstaculos
	menorX = min(lados[1])
	maiorX = max(lados[1])
	menorY = min(lados[0])
	maiorY = max(lados[0])
	#vertices comecam com menor X e menor Y
	vert = [inicio,[menorY,menorX]]
	#itera com base na quantidade de pontos. n(X) = n(Y)
	pontos = zip(lados[1], lados[0])	#insere em lista de pontos [[x1,y1],[xn,yn]]
	#pontos = list(set(list(pontos)))
	pontos = list(pontos)
	for item in range(len(lados[0])):		
		#se a distancia em X ou em Y ate o primeiro vertice for maior q o robo:
		if (pontos[item][0]-menorX > tamRobo) or (pontos[item][1]-menorY > tamRobo):
			vert.append(pontos[item])	#acrescenta ponto a lista de vertices
			#marca vertice atual como referencia (medir dist ate o proximo ponto (>tamRobo))
			menorX = pontos[item][0]	
			menorY = pontos[item][1]
	#vertices terminam com maior X e maior Y
	vert.append([maiorY,maiorX])
	vert.append(obj)
	
	for item in vert:
		cv2.circle(bordas,(item[0],item[1]),5,255,5)
		xis = str(item[0])
		ips = str(item[1])
		tudo = '('+xis+', '+ips+')'
		cv2.putText(bordas,tudo, (item[0],item[1]),cv2.FONT_HERSHEY_PLAIN, 1, 255,2)
	cv2.imwrite(nomeB+'.jpg',bordas)
	
	return vert	#retorna lista de coordenadas dos vertices: vert = [[x1,y1],[x2,y2],[xn,yn]]

v = vertices(inicio, jpg,obj)
texto = ''
for item in v:
	texto = texto+str(item)+'\n'
texto = texto[:-1]
arq = open(nome+'.txt','w')
arq.write(texto)
arq.close()

