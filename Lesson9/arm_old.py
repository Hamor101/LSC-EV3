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
