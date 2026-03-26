myVariable = 0

def bumper_b_pressed_callback_0():
    global myVariable
    Optical1.set_light(LedStateType.ON)
    Tread.spin(FORWARD, 2, VOLT)
    Wheel.spin(FORWARD, 4, VOLT)
    while (True):
        if Optical1.color() == Color.RED:
            Wheel.spin(FORWARD, 4, VOLT)
        elif Optical1.color() == Color.BLUE:
            Wheel.spin(REVERSE, 4, VOLT)
        else:
            wait(0.1, SECONDS)
        wait(5, MSEC)

# system event handlers
bumper_b.pressed(bumper_b_pressed_callback_0)
# add 15ms delay to make sure events are registered correctly.
wait(15, MSEC)
