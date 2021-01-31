import RPi.GPIO as gp
import socket
from Car import Car
from time import sleep
gp.setwarnings(False)

# set up visual LEDs
gp.setmode(gp.BCM)
gp.setup(17, gp.OUT) # green - controller connected
gp.setup(27, gp.OUT) # red - started server.py
gp.output(27, 1)
gp.output(17, 0)

# server setup
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = "192.168.1.130"
port = 1234
s.bind((host, port))
s.listen(1)

# accept connection
con,addr = s.accept()
print("connected: {}, {}".format(con, addr))
gp.output(17, 1)
connected = True

car = Car()

while 1:

	try:
		command = con.recv(1).decode()
		command = int(command)

		if command == 3:
			command = 10

		if command == 0:
			car.turnstraight()
			car.stop()

		# motor
		if command & 1:
			car.drivef()
		elif command & 2:
			car.driver()

		# turning
		if command & 4:
			car.turnl()
		elif command & 8:
			car.turnr()

	# controller disconnected
	except:
		connected = False
		print("controller disconnected")
		gp.output(17, 0)

		while not connected:

			# accept connection
			con,addr = s.accept()
			print("connected: {}, {}".format(con, addr))
			gp.output(17, 1)
			connected = True

		print("will retry in 3 seconds")
		sleep(3)
