from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, InfraredSensor, TouchSensor, ColorSensor
from pybricks.parameters import Port
from pybricks.robotics import DriveBase
from pybricks.tools import wait
ev3 = EV3Brick()

from barcode import ITFReader

left_motor = Motor(Port.B)
right_motor = Motor(Port.C)

robot = DriveBase(
    left_motor = left_motor,
    right_motor= right_motor,
    wheel_diameter=42.12,
    axle_track=105
)

color_sensor = ColorSensor(Port.S2)


def task_0():
    while True:
        print('Reflection:', color_sensor.reflection())
        print('Color:', color_sensor.color())
        print('Ambient:', color_sensor.ambient())
        print('Rgb:', color_sensor.rgb())
        print('#' * 50)
        wait(1000)

black, white = 7, 72

def task_1():
    angle = 40
    speed = 30 #mm/s
    tresh = (black + white) / 2
    while(True):
        if color_sensor.reflection() > tresh:
            robot.drive(speed, angle)
        else:
            robot.drive(speed, -angle)
            wait(10)
def task_2():
    max_turn = 70
    tresh = (black + white) / 2
    v = 30
    while True:
        r = color_sensor.reflection()
        t = (r - tresh) / (tresh - black) * max_turn
        robot.drive(v, t)
        print(t)
        wait(10)

def task_3():
    color_change_pts = []
    v = 35
    tresh = (black + white) / 2
    reader = ITFReader(10, 20)

    digits_to_read = 2
    code_length = 140
    robot.drive(v,0)
    v0 = False ## True = black | False = white
    while sum(color_change_pts) + robot.distance() < code_length:
        r = color_sensor.reflection()
        b = (r - tresh) < 0
        if b is not v0:
            print(robot.distance())
            if not color_change_pts:
                color_change_pts.append(0)
            else:
                color_change_pts.append(robot.distance())
            robot.reset()
            v0 = b
        wait(10)
    color_change_pts.append(robot.distance())
    print("Measured distances:", color_change_pts)
    n = reader.read(dists=color_change_pts[1:])
    print("Identified number:" + str(n))
    ev3.speaker.say(str(n))


if __name__ == "__main__":
    import sys
    globals()['task_' + sys.argv[1]]()

