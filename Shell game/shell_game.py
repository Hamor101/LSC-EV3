import logging
import random

from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, TouchSensor
from pybricks.parameters import Port, Button, Stop
from pybricks.tools import wait


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

BRICK = EV3Brick()
LEFT_ARM = Motor(port = Port.B)
RIGHT_ARM = Motor(port = Port.C)
REVEALER_ARM = Motor(port = Port.A)
RED_BUTTON = TouchSensor(port = Port.S1)


V_SW = 180 # °/s
V_REV = 150 # °/s

LEFT = -1
CENTER = 0
RIGHT = 1

BUTTON_DIR_MAP = {
    Button.LEFT: LEFT,
    Button.CENTER: CENTER,
    Button.RIGHT: RIGHT
}


WAIT_MS = 20

class ShellGame:
    def __init__(self):
        self.game_on = True
        self.level = 1
        self.ball_pos = CENTER

    def run(self):
        logger.info('Starting...')        
        while self.game_on:
            self.reveal()
            round_won = self.round()
            logger.info('Round won: %s', round_won)
            if round_won:
                self.level += 1
                logger.info('New level: %s', self.level)
            else:
                self.game_on = False
        self.reveal()
    
    def swap(self, a, v):
        a.run_angle(speed = v, rotation_angle=245, then = Stop.BRAKE)
        a.run_angle(speed = v, rotation_angle=-65, then = Stop.BRAKE)
        if (self.ball_pos == LEFT and a == LEFT_ARM or self.ball_pos == CENTER and a == RIGHT_ARM):
            self.ball_pos += 1 
        elif (self.ball_pos == CENTER and a == LEFT_ARM or self.ball_pos == RIGHT and a == RIGHT_ARM) :
            self.ball_pos -= 1
        else:
            pass
        logger.debug('Ball position: %s', self.ball_pos)


    def shuffle(self):
        logger.info('Shuffling')
        for _ in range(self.level):
            arm = random.choice((LEFT_ARM, RIGHT_ARM))
            self.swap(arm, V_SW* (1+(self.level-1)/10))

    def armUp(self):
        REVEALER_ARM.run_until_stalled(speed = V_REV, duty_limit=30, then=Stop.BRAKE)

    def armDown(self):
        REVEALER_ARM.run_until_stalled(speed = -V_REV, duty_limit=30, then=Stop.BRAKE)

    def reveal(self):
        if self.ball_pos == LEFT:
            self.swap(LEFT_ARM, V_SW)
        elif self.ball_pos == RIGHT:
            self.swap(RIGHT_ARM, V_SW)
        
        self.armUp()

        while not RED_BUTTON.pressed():
            wait(WAIT_MS)

 #      self.armDown()

    def guess(self):
        self.armDown()
        pressed = []
        while not pressed:
            pressed = BRICK.buttons.pressed()
            if (len(pressed) != 1 
                or (len(pressed) == 1 and pressed[0] not in (Button.LEFT, Button.CENTER, Button.RIGHT))
                ):
                pressed = []
            wait(WAIT_MS)
        choice = BUTTON_DIR_MAP[pressed[0]]
        logger.info('Guess: %s', choice)
        return choice

    def round(self):
        self.armDown()
        self.shuffle()
        g = self.guess()
        return g == self.ball_pos

if __name__ == "__main__":
    ShellGame().run()