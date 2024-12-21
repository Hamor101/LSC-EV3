import socket

from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, InfraredSensor
from pybricks.parameters import Port

ev3 = EV3Brick()

motor = Motor(Port.A)
dsensor = InfraredSensor(Port.S1)

address = '0.0.0.0'
port = 8000


def main():
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((address, port))
    s.listen(1)
    print('Running')
    while True:
        cl, addr = s.accept()
        #print('Connection from: %s' % addr)
        while True:
            line = cl.readline()
            if not line:
                break
            deg = int(line)
            motor.track_target(deg)
            dist = dsensor.distance()
            response = '{}\n'.format(dist)
            cl.send(response)
        cl.close()

main()