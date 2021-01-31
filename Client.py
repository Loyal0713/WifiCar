import socket
import RPi.GPIO as gp

from gpiozero import Button
from time import sleep

# set up connection light - off/disconnected, on/connected
gp.setmode(gp.BCM)
gp.setup(26, gp.OUT)
gp.output(26, 0)

# button setup
f = Button(17)
r = Button(27)
l = Button(22)
ri = Button(23)

# server setup and connect
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = "192.168.1.130"
port = 1234
s.connect((host, port))
connected = True

# update led
gp.output(26, 1)

command = 0

# run until you die >:)
while 1:

	try:

		# build command
		command = f.is_pressed + 2* r.is_pressed + 4*l.is_pressed + 8*ri.is_pressed

		# filter out invalid commands
		if command == 12:
			command = 0
		if command == 3:
			command = 0
		if command == 10:
			command = 3

		# send command
		#if command != 0:
			# print("client command: {}".format(command))

		s.send(str(command).encode())
		command = 0

		# add delay to prevent latency?????
		sleep(.01)

	# oh no disconnection
	except socket.error:
		print("oh no we got disconnected")
		connected = False
		gp.output(26, 0)
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

		# try to reconnect
		while not connected:
			try:
				s.connect((host, port))
				gp.output(26,1)
				connected = True
				print("we done did it boyz, run 'er back")
			except socket.error:
				print("retry in 3 secs")
				sleep(3)
