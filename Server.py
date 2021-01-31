import RPi.GPIO as gp
import socket
from Car import Car
from time import sleep
gp.setwarnings(False)

# set up visual LEDs
green = 17
red = 27
gp.setmode(gp.BCM)
gp.setup(green, gp.OUT) # green - controller connected
gp.setup(red, gp.OUT) # red - running server.py
gp.output(red, 1)
gp.output(green, 0)

# server setup
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = "192.168.1.130"
port = 1234
s.bind((host, port))
s.listen(1)

# accept connection
con,addr = s.accept()
gp.output(17, 1) # turn on controller status led
connected = True

# main loop
car = Car()
while 1:

	try:
        # receive and format command to int
		command = con.recv(1).decode()
		command = int(command)

        # update 3 to 10
		if command == 3:
			command = 10

        # stationary command
		if command == 0:
			car.turnstraight()
			car.stop()

		# motor commands
		if command & 1:
			car.drivef()
		elif command & 2:
			car.driver()

		# turning commands
		if command & 4:
			car.turnl()
		elif command & 8:
			car.turnr()

	# controller disconnected
	except:
		connected = False
		gp.output(green, 0) # update controller led

		while not connected:
			con,addr = s.accept() # reconnected
			gp.output(green, 1) # update controller led
			connected = True
