import logging
import threading


from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (
    Motor,
    TouchSensor
)
from pybricks.parameters import Port, Direction, Button
from pybricks.tools import wait

from .g_code import GCode

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

def run_g_code():
    ...


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
        logger.debug(f'Calibrating, ready: {len(calibrated_motors)}')
        wait(1000)


    run_g_code()
    

if __name__ == "__main__":
    main()