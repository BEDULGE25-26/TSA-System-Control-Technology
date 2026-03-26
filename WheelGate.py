myVariable = 0

def when_started1():
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

when_started1()
