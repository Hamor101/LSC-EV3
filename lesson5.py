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

robot = DriveBase(
    left_motor = left_motor,
    right_motor= right_motor,
    wheel_diameter=42.12,
    axle_track=105
)
def server():
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('0.0.0.0', 8000))
    s.listen(1) ## How many connections to accept
    try:
        while True:
            cl, addr = s.accept()
            print('Connections from ', addr)
            while True:
                line = cl.readline()
                print(line)
                if not line or line == b'\r\n':
                    break
            response = 'Distance: ' + str(dist_sensor.distance())
            
            cl.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
            cl.send(response)
            cl.close()
    except KeyboardInterrupt:
        sys.exit(0)
    finally:
        s.close()

def main():
    server()

main()