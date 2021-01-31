import socket
import RPi.GPIO as gp
from gpiozero import Button
from time import sleep

# set up connection light - off/disconnected, on/connected
led = 26
gp.setmode(gp.BCM)
gp.setup(led, gp.OUT)
gp.output(led, 0)

# button setup
f = Button(17) # forward
r = Button(27) # reverse
l = Button(22) # left
ri = Button(23)# right

# socket setup and connect
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = "192.168.1.130"
port = 1234
s.connect((host, port))
connected = True

# update led
gp.output(26, 1)

# main loop
command = 0
while 1:

	try:

		# build command
		command = f.is_pressed + 2*r.is_pressed + 4*l.is_pressed + 8*ri.is_pressed

		# filter out invalid commands
		if command == 12: # left and right
			command = 0
		if command == 3: # forward and back
			command = 0
		if command == 10: # cant send 10, set to 3 as 3 is not used as a valid command
			command = 3

		s.send(str(command).encode())
		command = 0 # reset command

		# add delay
		sleep(.01)

	# disconnected from server, try to reconnect
	except socket.error:
		connected = False
		gp.output(led, 0) # turn off led
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

		# try to reconnect
		while not connected:
			try:
				s.connect((host, port))
				gp.output(led,1) # turn on led
				connected = True
			except socket.error:
				sleep(3) # retry every 3 seconds
