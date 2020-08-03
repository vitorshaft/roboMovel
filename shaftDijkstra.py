import cv2
import numpy as np
import math
import sys

tamRobo = 30	#maior dimensao 2D do robo em cm
S = [10,10]	#coordenadas do inicio
G = [150,150]	#coordenadas do objetivo
arqMapa = 'mapa.jpg'	#arquivo JPG com o mapa de obstaculos

class no:
	def __init__(self,ind,x,y):
		self.dist = sys.maxsize
		self.coord = [x,y]
		self.noAdj = []
		self.visitado = False
		self.indice = ind
		self.anterior = None

class aresta:
	def __init__(self,v1,v2): #v1 e v2 sao as coordenadas [x,y] dos vertices
		co = v2[1]-v1[1]
		ca = v2[0]-v1[0]
		self.p1 = v1
		self.p2 = v2
		self.tam = math.hypot(co,ca)
		self.ind = None

def mostrar(imagem):
	cv2.imshow("imagem",imagem)
	cv2.waitKey(0)
	cv2.destroyAllWindows()

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
	"""
	for item in vert:
		cv2.circle(bordas,(item[0],item[1]),5,255,5)
		xis = str(item[0])
		ips = str(item[1])
		tudo = '('+xis+', '+ips+')'
		cv2.putText(bordas,tudo, (item[0],item[1]),cv2.FONT_HERSHEY_PLAIN, 1, 255,2)
	mostrar(bordas)
	"""
	return vert	#retorna lista de coordenadas dos vertices: vert = [[x1,y1],[x2,y2],[xn,yn]]

def edges(imagem,lista):	#lista de vertices[[x1,y1],[xn,yn]]
	arestas = []
	solidos = cv2.imread(imagem)	#matriz imagem do mapa de obstaculos
	#para cada vertice:
	for v1 in lista:
		#pega distancias entre vertices em X e Y
		for v2 in lista:
			dX = v2[0]-v1[0]
			dY = v2[1]-v1[1]
			#calcula distancia linear entre v1 e v2
			dist = int(math.hypot(dX,dY))
			#discretizacao dos pontos da linha v1/v2 (10 pontos)
			passoX = dX/10
			passoY = dY/10
			#faz 10 plotagens ao longo da linha e checa se a linha intercepta obstaculo
			for a in range(10):
				#print(solidos[v1[0]+(a*int(passoX)),v1[1]+(a*int(passoY))])
				if solidos[v1[0]+(a*int(passoX)),v1[1]+(a*int(passoY))][0] == 255:
				#se o segmento partindo de v1 interceptar, distancia = infinita
					dist = sys.maxsize
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
	return arestas	#arestas = [

#vertices([10,10],'mapa.jpg',[150,150])

nodes = vertices(S,arqMapa,G)
#grafo = [nodes[0]]
grafo = []	#inicia lista de nos
#i = 1
#cria lista de objetos (nos)
for item in range(len(nodes)):
	#nodes.pop(0)
	n = no(item,nodes[item][0],nodes[item][1])
	grafo.append(n)

edg = edges(arqMapa,nodes)	#cria lista de arestas entre os nos do grafo

#gerar nos adjacentes:
for a in edg:	#a cada aresta temos dois nos
	for n in grafo:	#procura um no no grafo...
		if n.coord == a.p1:	#...que coincida com o p1 da aresta
			ad = nodes.index(a.p2)
			n.noAdj.append(grafo[ad])	#adiciona o p2 como adjacente de p1
		elif n.coord == a.p2:	#mas se o no coincidir com o p2...
			ad = nodes.index(a.p1)
			n.noAdj.append(grafo[ad])	#adiciona o p1 com o adjacente de p2

"""PSEUDOCODIGO"""
for n in grafo:
	n.dist = sys.maxsize
nv = []
g = grafo [-1]
s = grafo[0]
s.dist = 0
#s.visitado = True

for n in grafo:
	if n.visitado == False:
		nv.append(n)
while nv != []:
	atual = no(sys.maxsize,sys.maxsize,sys.maxsize)
	for noh in nv:
		if noh.visitado == False and noh.dist < atual.dist:
			atual = noh
	atual.visitado = True
	nv.remove(atual)
	for adj in atual.noAdj:	#para cada no adjacente ao atual
		if adj.dist > (atual.dist+aresta(adj.coord,atual.coord).tam):
			adj.dist = atual.dist+aresta(adj.coord,atual.coord).tam
			adj.anterior = atual
			#lista.append(adj)
caminho = [grafo[-1]]
while (True):
	caminho.append(caminho[0].anterior)
print(caminho)

"""
lista = []
lista.append(s)
#while len(lista) != 0:

while lista != []:
	atual = no(sys.maxsize,sys.maxsize,sys.maxsize)
	for item in lista:
		if 	item.dist < atual.dist:
			atual = item
	lista.remove(atual)

#for node in grafo:
#for node in lista:	#a cada no na lista:
	for adj in atual.noAdj:	#para cada no adjacente ao atual
		if adj.dist > (node.dist+aresta(adj,node).tam):
			adj.dist = node.dist+aresta(adj,node).tam
			lista.append(adj)
"""
	
