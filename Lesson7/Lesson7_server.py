from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, InfraredSensor, TouchSensor, ColorSensor
from pybricks.parameters import Port
from pybricks.robotics import DriveBase
from pybricks.tools import wait
import socket
import sys
ev3 = EV3Brick()

left_motor = Motor(Port.B)
right_motor = Motor(Port.C)
dist_sensor = InfraredSensor(Port.S1)
color_sensor = ColorSensor(Port.S2)

robot = DriveBase(
    left_motor = left_motor,
    right_motor= right_motor,
    wheel_diameter=42.12,
    axle_track=105
)

address = '0.0.0.0'
port = 8000

body = """<!DOCTYPE html>
<html>
<body style = "background-color:{hex};"></body>
<h1>{hex}</h>
</body>
</html>
"""
def server():
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('0.0.0.0', port))
    s.listen(1)
    
    try:
        while True:
            cl, addr = s.accept()
            print('Connections from ', addr)
            line = cl.readline()
            print(line)
            cl.send('0')
            cl.close()
            speed, turn = line.decode('utf-8').split()
            robot.drive(int(speed), int(turn))

    except KeyboardInterrupt:
        sys.exit(0)
    finally:
        s.close()

server()