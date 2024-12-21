from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (
    Motor,
    TouchSensor
)
from pybricks.parameters import Port, Direction, Button
from pybricks.tools import wait

ev3 = EV3Brick()
motor_turn = Motor(
    port = Port.C,
    positive_direction= Direction.CLOCKWISE,
    gears=[12, 36]
)

motor_raise = Motor(
    port = Port.B,
    positive_direction= Direction.COUNTERCLOCKWISE,
    gears=[12, 36]
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


def manual_control():
    spd = 120
    spdv = 90
    v_grip = 20
    motor_grip.run_until_stalled(speed=v_grip)
    motor_grip.run_angle(-v_grip, 90)
    grip_closed = False
    while True:
        pressed = ev3.buttons.pressed()
        if not pressed:
            motor_turn.hold()
            motor_raise.hold()
        if len(pressed) != 1:
            continue
        b = pressed[0]
        if b == Button.LEFT:
            motor_turn.run(-spd)
        elif b == Button.RIGHT:
            motor_turn.run(spd)
        elif b == Button.UP:
            motor_raise.run(spdv)
        elif b == Button.DOWN:
            motor_raise.run(-spdv)
        elif b == Button.CENTER:
            motor_grip.run_until_stalled(speed=v_grip) ## close
            motor_grip.run_angle(-v_grip, 90) ## open
    wait(50)
        
    # print(pressed) --> [BUTTON.LEFT, BUTTON.RIGHT]

def manu2():
    v = 90
    bstate = {
        Button.LEFT: False,
        Button.RIGHT: False,
        Button.UP: False,
        Button.DOWN: False
    }
    while True:
        bp = ev3.buttons.pressed()
        for i in bstate:
            bstate[i] = i in bp
        vt = v * (bstate[Button.LEFT] - bstate[Button.RIGHT])
        vr = v * (bstate[Button.UP] - bstate[Button.DOWN])
        motor_turn.run(vt)
        motor_raise.run(vr)

def main():
    manu2()
    

if __name__ == "__main__":
    main()