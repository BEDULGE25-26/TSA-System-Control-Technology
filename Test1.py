from vex import *
import urandom
import math

brain=Brain()

bottomTread = Motor(Ports.PORT1, GearSetting.RATIO_18_1, True)
optical2x2 = Optical(Ports.PORT2)
startBumper = Bumper(brain.three_wire_port.a)
wheel2x2 = Motor(Ports.PORT3, GearSetting.RATIO_18_1, True)
topTread = Motor(Ports.PORT4, GearSetting.RATIO_18_1, True)
wheel3x2 = Motor(Ports.PORT5, GearSetting.RATIO_18_1, True)
optical3x2 = Optical(Ports.PORT6)
catchError2x2 = Optical(Ports.PORT7)
catchError3x2 = Optical(Ports.PORT8)

wait(30, MSEC)

def initializeRandomSeed():
    wait(100, MSEC)
    random = brain.battery.voltage(MV) + brain.battery.current(CurrentUnits.AMP) * 100 + brain.timer.system_high_res()
    urandom.seed(int(random))
      
initializeRandomSeed()

def convert_color_to_string(col):
    if col == Color.RED:
        return "red"
    if col == Color.GREEN:
        return "green"
    if col == Color.BLUE:
        return "blue"
    if col == Color.WHITE:
        return "white"
    if col == Color.YELLOW:
        return "yellow"
    if col == Color.ORANGE:
        return "orange"
    if col == Color.PURPLE:
        return "purple"
    if col == Color.CYAN:
        return "cyan"
    if col == Color.BLACK:
        return "black"
    if col == Color.TRANSPARENT:
        return "transparent"
    return ""

def play_vexcode_sound(sound_name):
    print("VEXPlaySound:" + sound_name)
    wait(5, MSEC)

wait(200, MSEC)
print("\033[2J")

screen_precision = 0
console_precision = 0
redCount = 0
blueCount = 0
errorCountRed = 0
errorCountBlue = 0

def when_started1():
    global redCount, blueCount, errorCountRed, errorCountBlue, screen_precision, console_precision
    while (True):
        if startBumper.pressing():
            wait(1, SECONDS)
            blueCount = 0
            redCount = 0
            errorCountRed = 0
            errorCountBlue = 0
            topTread.spin(FORWARD, 2, VOLT)
            bottomTread.spin(FORWARD, 1.8, VOLT)
            wheel2x2.spin(FORWARD, 1, VOLT)
            wheel3x2.spin(FORWARD, 1, VOLT)
            optical2x2.set_light(LedStateType.ON)
            optical3x2.set_light(LedStateType.ON)
            catchError2x2.set_light(LedStateType.ON)
            catchError3x2.set_light(LedStateType.ON)
            while not ((blueCount + redCount + errorCountRed + errorCountBlue) == 24):
                if catchError3x2.color() == Color.BLUE:
                    blueCount = blueCount + 1
                elif catchError3x2.color() == Color.RED:
                    errorCountRed = errorCountRed + 1
                else:
                    wait(0.001, SECONDS)
                if catchError2x2.color() == Color.RED:
                    redCount = redCount + 1
                elif catchError2x2.color() == Color.BLUE:
                    errorCountBlue = errorCountBlue + 1
                else:
                    wait(0.001, SECONDS)
                if optical2x2.color() == Color.RED:
                    wheel2x2.spin(FORWARD, 1, VOLT)
                elif optical2x2.color() == Color.BLUE:
                    wheel2x2.spin(REVERSE, 1, VOLT)
                else:
                    wait(0.001, SECONDS)
                if optical3x2.color() == Color.RED:
                    wheel3x2.spin(FORWARD, 1, VOLT)
                elif optical3x2.color() == Color.BLUE:
                    wheel3x2.spin(REVERSE, 1, VOLT)
                else:
                    wait(0.001, SECONDS)
                if startBumper.pressing():
                    continue
                wait(5, MSEC)
            if startBumper.pressing():
                continue
            bottomTread.stop()
            topTread.stop()
            wheel2x2.stop()
            wheel3x2.stop()
            optical2x2.set_light(LedStateType.OFF)
            optical3x2.set_light(LedStateType.OFF)
            catchError2x2.set_light(LedStateType.OFF)
            catchError3x2.set_light(LedStateType.OFF)
            errorCountRed += (4 - redCount)
            errorCountBlue += (6 - blueCount)
            brain.screen.set_cursor(1, 1)
            brain.screen.print("Correct Red Blocks: " + redCount)
            brain.screen.next_row()
            brain.screen.print("Incorrect Red Blocks: " + errorCountRed)
            brain.screen.next_row()
            brain.screen.print("Correct Blue Blocks: " + blueCount)
            brain.screen.next_row()
            brain.screen.print("Incorrect Blue Blocks: " + errorCountBlue)
            brain.screen.next_row()
        wait(0.1, SECONDS)
        wait(5, MSEC)

when_started1()
