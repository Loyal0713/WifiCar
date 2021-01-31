import RPi.GPIO as gp

class Car:
	def __init__(self):
        # set vars for l293d driver
		self.in1 = 5
		self.in2 = 6
		self.in3 = 13
		self.in4 = 19
		self.enable = 26

		gp.setmode(gp.BCM) # set board mode and setup driver pins
		gp.setup(self.enable, gp.OUT)
		gp.setup(self.in1, gp.OUT)
		gp.setup(self.in2, gp.OUT)
		gp.setup(self.in3, gp.OUT)
		gp.setup(self.in4, gp.OUT)

        # setup and initialize pwms for driver pins
		self.forward = gp.PWM(self.in1, 100)
		self.reverse = gp.PWM(self.in2, 100)
		self.left = gp.PWM(self.in3, 100)
		self.right = gp.PWM(self.in4, 100)
		self.forward.start(0)
		self.reverse.start(0)
		self.left.start(0)
		self.right.start(0)

		gp.output(self.enable, gp.HIGH) # enable enable pin

    # functions to define car actions: drive forward, drive reverse, stop,
    # turn left,turn right, turn straight
	def drivef(self):
		self.forward.ChangeDutyCycle(100)
		self.reverse.ChangeDutyCycle(0)
	def driver(self):
		self.reverse.ChangeDutyCycle(100)
		self.forward.ChangeDutyCycle(0)
	def stop(self):
		self.reverse.ChangeDutyCycle(0)
		self.forward.ChangeDutyCycle(0)
	def turnl(self):
		self.left.ChangeDutyCycle(100)
		self.right.ChangeDutyCycle(0)
	def turnr(self):
		self.right.ChangeDutyCycle(100)
		self.left.ChangeDutyCycle(0)
	def turnstraight(self):
		self.right.ChangeDutyCycle(0)
		self.left.ChangeDutyCycle(0)
