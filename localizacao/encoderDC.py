from gpiozero import Button

irEsq = Button(3)
irDir = Button(2)
pDir = 0
pEsq = 0

def contadorD():
	inicio = 0
	if irDir.wait_for_press():
		return 1
	elif irDir.wait_for_release():
		return 1

while True:
	pDir+=contadorD()
	print pDir
