import face_recognition
import cv2
import numpy as np

class identificar:
	def __init__(self):
		self.video_capture = cv2.VideoCapture(1)
		#   CARREGA UMA IMAGEM DE AMOSTRA E APRENDE A RECONHECE-LA.
		self.vitor_image = face_recognition.load_image_file("/home/pi/roboMovel/busca/exemplo.jpg")
		self.vitor_face_encoding = face_recognition.face_encodings(self.vitor_image)[0]
	
		#   CRIA ARRAYS DE CODIFICACAO DE FACES CONHECIDAS E SEUS NOMES
		self.known_face_encodings = [
			self.vitor_face_encoding,
		]
		self.known_face_names = [
			"Vitor"
		]
	
		#   INICIALIZACAO DE VARIAVEIS
		self.face_locations = []
		self.face_encodings = []
		self.face_names = []
		
	
	def comparar(self):
		self.process_this_frame = True
		#while(True):
									
		#   PEGA UM QUADRO DO VIDEO
		self.ret, self.frame = self.video_capture.read()
		#   REDIMENSIONA O QUADRO PARA 1/4 DO TAMANHO PARA ACELERAR O RECONHECIMENTO
		self.small_frame = cv2.resize(self.frame, (0, 0), fx=0.25, fy=0.25)
		#   CONVERTE A IMAGEM DE BGR PARA RGB (DE OPENCV PARA FACE_RECOGNITION)
		self.rgb_small_frame = self.small_frame[:, :, ::-1]
		
		# Only process every other frame of video to save time
		if self.process_this_frame:
		#    ENCONTRA TODAS AS FACES E SUAS CODIFICACOES NO QUADRO ATUAL
			self.face_locations = face_recognition.face_locations(self.rgb_small_frame)
			self.face_encodings = face_recognition.face_encodings(self.rgb_small_frame, self.face_locations)
		
			self.face_names = []
			for self.face_encoding in self.face_encodings:
				# VE SE O ROSTO COINCIDE COM OS ROSTOS CONHECIDOS
				self.matches = face_recognition.compare_faces(self.known_face_encodings, self.face_encoding)
				self.name = "Unknown"
		
				# # If a match was found in known_face_encodings, just use the first one.
				# if True in matches:
				#     first_match_index = matches.index(True)
				#     name = known_face_names[first_match_index]
		
				# Or instead, use the known face with the smallest distance to the new face
				self.face_distances = face_recognition.face_distance(self.known_face_encodings, self.face_encoding)
				self.best_match_index = np.argmin(self.face_distances)
				if self.matches[self.best_match_index]:
					self.name = self.known_face_names[self.best_match_index]
		
				self.face_names.append(self.name)
		
			self.process_this_frame = not self.process_this_frame
		
		
			# Display the results
			for (top, right, bottom, left), name in zip(self.face_locations, self.face_names):
			# Scale back up face locations since the frame we detected in was scaled to 1/4 size
				top *= 4
				right *= 4
				bottom *= 4
				left *= 4
				center = (right+left)/2
				altura = bottom-top
				centro = (right+left)/2
				return [altura,centro]
			#cv2.imshow('Video', self.small_frame)
			
			
		else:
			return 'objetivo nao encontrado'
			#cv2.imshow('Video', self.small_frame)
			
		    
		
		
