import logging
import threading
import sys

from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (
    Motor,
    TouchSensor
)
from pybricks.parameters import Port, Direction, Button
from pybricks.tools import wait

from g_code import GCode

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

def run_g_code(c):
   GCodeRunner(c).run()


class GCodeRunner:
    def __init__(self, code: GCode):
        self.code = code
        self.max_speed = 100 # °/s
        self.feed_speed = self.max_speed

        self.m_x = motor_turn
        self.m_y = motor_raise
        self.m_z = motor_grip

    def run(self):
        for cl in self.code.lines:
            if cl.command == ('M', 30):
                sys.exit(0)
            elif cl.command[0] == 'F':
                self.set_feed(cl.command[1])
            elif cl.command[0] == 'G':
                cn = cl.command[1]
                if cn == 0:
                    self.move(**cl.params, v = self.max_speed)
                elif cn == 1:
                     self.move(**cl.params, v = self.feed_speed)
                elif cn == 28:
                    self.move(0, 0, 0, self.max_speed)
                elif cn == 4:
                    self.wait(**cl.params)
                else:
                    raise ValueError("Unknown G command")
            else:
                raise ValueError("Unknown command")

    def set_feed(self, speed):
        self.feed_speed = speed

    def wait(self, p=0, s=0):
        p = p + s*1000
        wait(p)

    def move(self, x=None, y=None, z=None, v=None):
        x0 = self.m_x.angle()
        y0 = self.m_y.angle()
        z0 = self.m_z.angle()


        x = x if x is not None else x0
        y = y if y is not None else y0
        z = z if z is not None else z0

        dx = x - x0
        dy = y - y0
        dz = z - z0

        s = (dx**2 + dy ** 2 + dz ** 2) ** 0.5
        t = s/v

        vx = dx/t
        vy = dy/t
        vz = dz/t

        self.m_x.run(dx)
        self.m_y.run(dy)
        self.m_z.run(dz)


        ok = {"x": dx == 0, "y" : dy == 0, "z": dz == 0}
        while not all(ok.values()):
            xa = self.m_x.angle()
            ya = self.m_y.angle()
            za = self.m_z.angle()

            if vx > 0 and xa >= x or vx < 0 and xa <= x:
                self.m_x.hold()
                ok['x'] = True

            if vy > 0 and ya >= y or vy < 0 and ya <= y:
                self.m_y.hold()
                ok['y'] = True

            if vz > 0 and za >= z or vz < 0 and za <= z:
                self.m_z.hold()
                ok['z'] = True




def main():
    logger.info('Starting')
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
    else:
        logger.error("No file provided")
        sys.exit(1)
    #calibrate(motor_turn, sensor_turn.pressed, 183, 90)
    #calibrate(motor_raise, sensor_raise.pressed, 45, 0)
    #calibrate(motor_grip, motor_grip.stalled, 0, -90)
    th = threading.Thread(target=calibrate, args =(motor_turn, sensor_turn.pressed, 100, 0))
    th.start()
    th2 = threading.Thread(target = calibrate, args = (motor_raise, sensor_raise.pressed, 45, 0))
    th2.start()
    th3 = threading.Thread(target = calibrate, args = (motor_grip, motor_grip.stalled, 0, -90))
    th3.start()
    while len(calibrated_motors) < 3:
        #logger.debug('Calibrating, ready: %s')
        wait(1000)

#    logger.info(f"Reading file {file_path}")

    with open(file_path) as fp:
        g_code = GCode(fp.read())

    run_g_code(g_code)
    

if __name__ == "__main__":
    main()