from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, InfraredSensor, TouchSensor
from pybricks.parameters import Port
from pybricks.robotics import DriveBase
from pybricks.tools import wait
ev3 = EV3Brick()

left_motor = Motor(Port.B)
right_motor = Motor(Port.C)

robot = DriveBase(
    left_motor = left_motor,
    right_motor= right_motor,
    wheel_diameter=42.12,
    axle_track=105
)



def square(l):
    for _ in range(4):
        robot.straight(l)
        robot.turn(90)


def task_1():
   square(100)

def triangle(l):
    for _ in range(3):
        robot.straight(l)
        robot.turn(120)

def polygon(n,l):
    for _ in range(n):
        robot.straight(l)
        robot.turn(360/n)

def task_2():
    triangle(100)

def task_3():
    polygon(6, 100)

def task_4():
    square(100)
    robot.turn(90)
    triangle(100)
    robot.turn(-90)

dist_sensor = InfraredSensor(Port.S1)

def task_5():
    thresh = 20
    robot.drive(100,0)
    while(True):
        if dist_sensor.distance() < thresh:
            robot.turn(90)
            robot.straight(100)
            robot.turn(-90)
            robot.drive(100,0)
        wait(10)

touchsensor = TouchSensor(Port.S4)

def task_6():
    thresh = 20
    v = 100
    robot.drive(v, 0)
    while(True):
        if dist_sensor() < thresh:
            robot.drive(-v, 0)
        if touchsensor.pressed():
            robot.drive(v, 0)

def task_7():
    thresh = 20
    v = 100
    if dist_sensor.distance > thresh:
        robot.drive(v* (dist_sensor.distance - thresh),0)
    else:
        robot.drive(-v* (dist_sensor.distance - thresh), 0)

def task_8():
    d = 30
    v = 500
    while True:
        dist_diff_ratio = (dist_sensor.distance() - d) / d
        if dist_diff_ratio > 1:
            robot.drive(0, 0)
        else:
            robot.drive(v*dist_diff_ratio, 0)
        wait(10)

import threading

def task_9():
    import time
    def count_1():
        c = 0
        while True:
            print('c1', c)
            c+=1
            time.sleep(1)
    def count_2():
        c = 0
        while True:
            print('c2', c)
            c+=1
            time.sleep(1.5)
    t1 = threading.Thread(target=count_1)
    #t2 = threading.Thread(target=count_2)
    t1.start()
    #t2.start()
    count_2()

def task_10():
    d = 20
    v = 100
    ddr = 1
    def setddr():
        nonlocal ddr
        while True:
            ddr = (dist_sensor.distance() - d) / d
            wait(10)
    t1 = threading.Thread(target=setddr)
    t1.start()
    while True:
        if ddr > 1:
            robot.drive(0, 0)
        else:
            robot.drive(v*ddr, 0)
if __name__ == '__main__':
    import sys
    print(sys.argv)
    globals()['task_' + sys.argv[1]]()
    