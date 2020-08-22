#import cv2
import numpy as np
import math
import sys
import json

tamRobo = 30	#maior dimensao 2D do robo em cm
#S = [10,10]	#coordenadas do inicio
#G = [240,60]	#coordenadas do objetivo
#arqMapa = 'mapa.jpg'	#arquivo JPG com o mapa de obstaculos
#arqVert = 'grafo_'+str(S[0])+'_'+str(S[1])+'_a'+str(G[0])+'_'+str(G[1])+'.txt'

entrada = input('insira os pontos de inicio e obj separados por espaco: ')
pts = entrada.split(' ')
S = [int(pts[0]),int(pts[1])]
G = [int(pts[2]),int(pts[3])]

gf = 'grafo.json'

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
"""
def mostrar(imagem):
	cv2.imshow("imagem",imagem)
	cv2.waitKey(0)
	cv2.destroyAllWindows()
"""
try:
	
	with open(gf) as jsonFile:
		data = json.load(jsonFile)
		nodes = data['vertices']
		d = data['arestas']
		rotas = d['arestas']
except:
	print("Grafo nao encontrado, execute python mapa_em_grafo.py <mapa.extensao>")
#print(rotas)
	
#vertices([10,10],'mapa.jpg',[150,150])

#nodes = vertices(S,arqMapa,G)
#grafo = [nodes[0]]
'''
nodes = []
a = open(arqVert,'r')
b = a.read()
a.close()
c = b.split('\n')
for item in c:
	e = item[1:-1].split(', ')
	nodes.append([int(e[0]),int(e[1])])
'''
grafo = []	#inicia lista de nos
#i = 1
#cria lista de objetos (nos)
for item in range(len(nodes)):
	#nodes.pop(0)
	n = no(item,nodes[item][0],nodes[item][1])
	grafo.append(n)

edg = []	#inicia lista de objetos aresta()

#print(rotas[0][0])
for ar in range(len(rotas)):
	arst = aresta(rotas[ar][0], rotas[ar][1])
	edg.append(arst)

#edg = edges(arqMapa,nodes)	#cria lista de arestas entre os nos do grafo

#gerar nos adjacentes:
for a in edg:	#a cada aresta temos dois nos
	for n in grafo:	#procura um no no grafo...
		if n.coord == a.p1:	#...que coincida com o p1 da aresta
			ad = nodes.index(a.p2)
			n.noAdj.append(grafo[ad])	#adiciona o p2 como adjacente de p1
		elif n.coord == a.p2:	#mas se o no coincidir com o p2...
			ad = nodes.index(a.p1)
			n.noAdj.append(grafo[ad])	#adiciona o p1 com o adjacente de p2
#for n in grafo:
	#print(n.noAdj)

"""DIJKSTRA"""
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
'''
for item in grafo:
	print(item.visitado)
'''	
#while nv != []:
atual = no(sys.maxsize,sys.maxsize,sys.maxsize)
for noh in nv:
	if noh.visitado == False: #and noh.dist < atual.dist:
		atual = noh
		#print(atual.coord)
	atual.visitado = True
	#nv.remove(atual)
	#print('loop de escolha da menor aresta adj')
	for adj in atual.noAdj:	#para cada no adjacente ao atual
		if adj.dist > (atual.dist+aresta(adj.coord,atual.coord).tam) and adj.visitado == False:
			adj.dist = atual.dist+aresta(adj.coord,atual.coord).tam
			adj.anterior = atual
		#lista.append(adj)
print('gerando caminho')
caminho = []

for v in grafo[1:]:
	nAnt = v.anterior
	try:
		#print(nAnt.coord)
		if nAnt.coord != S:
			caminho.append(nAnt.coord)
	except:
		#print(nAnt)
		pass
#print(caminho[:-1])
#caminho = list(dict.fromkeys(caminho))
for item in caminho:
	for i in range(caminho.count(item)-1):
		caminho.remove(item)
print("nos entre S e G: ",caminho)
rotas = {}
rotas[entrada] = [0]
rotas[entrada] = {entrada:caminho}
with open('caminho.json','w') as BD:
	json.dump(rotas,BD)
	BD.close()
