"""	EXECUTAR COM PYTHON 2		"""

#python mapa_em_grafo.py mapa.jpg

import cv2
import numpy as np
import math
import json
import argparse

ap = argparse.ArgumentParser(description= 'converte mapa em jpg para txt com obstaculos')
ap.add_argument(	'mapa', type=str, help= 'um endereco de arquivo jpg para leitura do mapa de obstaculos')
ap.add_argument(	'xisS', type=int)
ap.add_argument(	'ipsS', type=int)
ap.add_argument(	'xisG', type=int)
ap.add_argument(	'ipsG', type=int)
args = ap.parse_args()
print(args.mapa)

grafo = {}
grafo['vertices'] = [0]
grafo['arestas'] = [0]

class aresta:
	def __init__(self,v1,v2): #v1 e v2 sao as coordenadas [x,y] dos vertices
		co = v2[1]-v1[1]
		ca = v2[0]-v1[0]
		self.p1 = v1
		self.p2 = v2
		self.tam = math.hypot(co,ca)
		self.ind = None

jpg = args.mapa
tamRobo = 30
"""
entrada = raw_input('insira os pontos de inicio e obj separados por espaco: ')
pts = entrada.split(' ')
inicio = [int(pts[0]),int(pts[1])]
obj = [int(pts[2]),int(pts[3])]
"""
inicio = [args.xisS,args.ipsS]
obj = [args.xisG,args.ipsG]

# nome = pts[0]+'_'+pts[1]+'_a'+pts[2]+'_'+pts[3]
nome = '%d_%d_a%d_%d'%(args.xisS,args.ipsS,args.xisG,args.ipsG)
nomeV = 'grafo_'+nome
nomeB = 'bordas_'+nome
nomeA = 'arestas_'+nome
nomeJ = nome+'.json'

def vertices(inicio,imagem,obj):
	#parametros de deteccao de borda:
	inf = 0 
	sup = 255
	ker = 5
	espaco = 10	#espaco minimo entre vertices
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
	for item in range(len(lados[0])):	 #iteracao por quantidade de X	
		#se a distancia em X ou em Y ate o primeiro vertice for maior q o robo:
		if (pontos[item][0]-menorX > espaco) or (pontos[item][1]-menorY > espaco):
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

def edges(imagem,lista):	#lista de vertices[[x1,y1],[xn,yn]]
	arestas = []
	solidos = cv2.imread(imagem)	#matriz imagem do mapa de obstaculos
	branco = solidos[70,30] #deveria exibir [ 255 255 255]
	preto = solidos[30,70] #deveria ser [0 0 0]
	print(branco)
	print(preto)
	#para cada vertice:
	for v1 in lista:
		#pega distancias entre vertices em X e Y
		for v2 in lista:
			dX = v2[0]-v1[0]
			dY = v2[1]-v1[1]
			#calcula distancia linear entre v1 e v2
			dist = int(math.hypot(dX,dY))
			#discretizacao dos pontos da linha v1/v2 (10 pontos)
			passoX = dX/20
			passoY = dY/20
			#faz 10 plotagens ao longo da linha e checa se a linha intercepta obstaculo
			for a in range(20):
				#	coleta valor do pixel na posicao v1 mais 1 passo:
				amostra = solidos[v1[1]+(a*int(passoY)),v1[0]+(a*int(passoX))][0]
				#am = solidos[v1[0]+(a*int(passoX)),v1[1]+(a*int(passoY))]
				#print(amostra)
				#if v1 == [10,10]:
					#print(v1,v2,[v1[0]+(a*int(passoX)),v1[1]+(a*int(passoY))],am)
				if  amostra != 0:
				#se o segmento partindo de v1 interceptar, distancia = infinita
					dist = 1000000000
					break
					#print(v1,v2," descartado")
				#elif amostra !=255 and amostra != 0:
					#print([v1[0]+(a*int(passoX)),v1[1]+(a*int(passoY))],amostra)
			#f v1 == [10,10] and v2 == [220,62]:
			#	print(v1,v2,dist)
			#print(v1,v2,dist)
			if dist != 1000000000 and dist != 0:
				ar = aresta(v1,v2)
				try:
					ra = aresta(v2,v1)
					ind = arestas.index(ra)
					arestas.pop(ind)
				except:
					pass
				arestas.append(ar)
	for a in arestas:
		a.ind = arestas.index(a)
	return arestas

v = vertices(inicio, jpg,obj)
vt = v
for item in v:	#reordenando vertices
	vt[v.index(item)] = list(item)
#grafo['vertices'] = {'vertices':vt}
grafo['vertices'] = vt
'''
with open('grafo.json','w') as DB:
	print(grafo)
	json.dump(grafo,DB)
	DB.close()
'''

linhas = edges(jpg,v)

m = cv2.imread(jpg)
for t in linhas:
	cv2.line(m,(t.p1[0],t.p1[1]),(t.p2[0],t.p2[1]),(150,150,150),1)
cv2.imshow('grafo',m)
cv2.waitKey(0)
cv2.destroyAllWindows()

rotas = []
for a in linhas:
	rotas.append([a.p1,a.p2,int(a.tam),a.ind])
grafo['arestas'] = {'arestas':rotas}
print(grafo)

with open('grafo.json','w') as BD:
	json.dump(grafo,BD)
	BD.close()

