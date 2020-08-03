import board
import busio
import adafruit_vl53l0x

class laser:
	def __init__(self):
		self.i2c = busio.I2C(board.SCL, board.SDA)
		self.sensor = adafruit_vl53l0x.VL53L0X(self.i2c)
		#self.sensor.measurement_timing_budget = 200000 #mais preciso: 200 ms
	def dLaser(self):
		self.distLaser = self.sensor.range
		pub = open('/home/pi/roboMovel/laserTopic.txt','w')
		pub.write(str(self.distLaser/10))
		pub.close()
		return self.distLaser
