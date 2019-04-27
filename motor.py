import RPi.GPIO as GPIO
import time
GPIO.setwarnings(False)

class dispenser:
	
	def __init__(self, name):
		self.name = name
		
		GPIO.cleanup()
		GPIO.setmode(GPIO.BOARD)
		GPIO.setup(31,GPIO.OUT)
		GPIO.setup(33,GPIO.OUT)
		GPIO.setup(35,GPIO.OUT)
		GPIO.setup(37,GPIO.OUT)

		GPIO.output(31, False)
		GPIO.output(33, False)
		GPIO.output(35, False)
		GPIO.output(37, False)

	def dispense(self):
		
		for i in range(0, 256):
			
			self.setStep(1, 0, 0, 0)
			time.sleep(0.005)
			self.setStep(0, 1, 0, 0)
			time.sleep(0.005)
			self.setStep(0, 0, 1, 0)
			time.sleep(0.005)
			self.setStep(0, 0, 0, 1)
			time.sleep(0.005)
			
		time.sleep(0.25)
		
		for i in range(0, 256):
			
			self.setStep(1, 0, 0, 0)
			time.sleep(0.005)
			self.setStep(0, 1, 0, 0)
			time.sleep(0.005)
			self.setStep(0, 0, 1, 0)
			time.sleep(0.005)
			self.setStep(0, 0, 0, 1)
			time.sleep(0.005)
			
	def setStep(self, w1, w2, w3, w4):

		GPIO.output(31, w1)
		GPIO.output(33, w2)
		GPIO.output(35, w3)
		GPIO.output(37, w4)
