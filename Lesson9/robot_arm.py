from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (
    Motor,
    TouchSensor
)
from pybricks.parameters import Port, Direction
from pybricks.tools import wait

ev3 = EV3Brick()
motor_turn = Motor(
    port = Port.C,
    positive_direction= Direction.CLOCKWISE,
    gears=[12, 36]
)

motor_raise = Motor(
    port = Port.B
)

motor_grip = Motor(
    port = Port.A
)

sensor_turn = TouchSensor(port=Port.S1)
sensor_raise = TouchSensor(port=Port.S3)

def calibrate():
    motor_turn.run(30)
    while not sensor_turn.pressed():
        wait(50)
    motor_turn.hold()
    motor_turn.reset_angle(180)
    motor_turn.run_angle(-45, 90)

## asidhasudh

def main():
    calibrate()
    

if __name__ == "__main__":
    main()