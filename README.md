This project uses two Raspberry Pi's to control an old toy car. One pi acts as a server (car), the other acts as the client (controller).

The controller is wired to 4 buttons and one green LED. The LED lets the user know when it is connected to the server. The 4 buttons
build a command that is sent as a number to the server. The command is built by flipping bits depending on which buttons are pressed.
Invalid commands (forward and reverse or left and right pressed at the same time) are sent as 0. The command is processed at the server.

The car is wired to control two status LEDs and two motors. The red LED is turned on as soon as the Server.py program is run to let the
user know when the program starts. The green LED is turned on when a controller is connected and is turned off when connection is lost.
The server receives the command and interprets what needs to be done. By detecting which bits are active, the server tells the car what
action to take.

Car.py acts as an API to easily interface between the server and the actual car hardware.
