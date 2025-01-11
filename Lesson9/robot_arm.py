import logging
import threading


from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (
    Motor,
    TouchSensor
)
from pybricks.parameters import Port, Direction, Button
from pybricks.tools import wait

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

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

calibrated_motors = []


def calibrate(m : Motor, end_crit, resetAngle, finalAngle):
    m.run(60)
    while not end_crit():
        wait(50)
        
    m.hold()
    m.reset_angle(resetAngle)
    m.run_target(-90, finalAngle)
    calibrated_motors.append(m)

def manual_control():
    v = 45
    bstate = {
        Button.LEFT: False,
        Button.RIGHT: False,
        Button.UP: False,
        Button.DOWN: False
    }

    grip_dir = 1
    while True:
        bp = ev3.buttons.pressed()
        for i in bstate:
            bstate[i] = i in bp
        vt = v * (bstate[Button.RIGHT] - bstate[Button.LEFT])
        vr = v * (bstate[Button.UP] - bstate[Button.DOWN])
        if not (sensor_turn.pressed() and vt > 0):
            motor_turn.run(vt)
        if not (sensor_raise.pressed() and vr > 0):
            motor_raise.run(vr)
        
        grip_on = Button.CENTER in bp
        vg = v * grip_on * grip_dir

        motor_grip.run(vg)
        if motor_grip.stalled() and vg > 0 or motor_grip.angle() < -90 and vg <0:
            grip_dir *= -1
        
        vs = (vt, vr, vg)

        if any(vs):
            logger.debug('Turn: %s, Raise: %s, Grip: %s', motor_turn.angle(), motor_raise.angle(), motor_grip.angle())
        wait(20)




def main():
    logger.info('Starting')
    #calibrate(motor_turn, sensor_turn.pressed, 183, 90)
    #calibrate(motor_raise, sensor_raise.pressed, 45, 0)
    #calibrate(motor_grip, motor_grip.stalled, 0, -90)
    th = threading.Thread(target=calibrate, args =(motor_turn, sensor_turn.pressed, 183, 90))
    th.start()
    th2 = threading.Thread(target = calibrate, args = (motor_raise, sensor_raise.pressed, 45, 0))
    th2.start()
    th3 = threading.Thread(target = calibrate, args = (motor_grip, motor_grip.stalled, 0, -90))
    th3.start()
    while len(calibrated_motors) < 3:
        wait(1000)
        print(len(calibrated_motors), end='\r')

    manual_control()
    

if __name__ == "__main__":
    main()