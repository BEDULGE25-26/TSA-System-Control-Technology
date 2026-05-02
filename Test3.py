from vex import *
import urandom
import math

brain = Brain()

bottomTread       = Motor(Ports.PORT5, GearSetting.RATIO_18_1, True)
topTread          = Motor(Ports.PORT1, GearSetting.RATIO_18_1, True)
optical2x2        = Optical(Ports.PORT4)
wheel2x2          = Motor(Ports.PORT3, GearSetting.RATIO_18_1, True)
optical3x2        = Optical(Ports.PORT6)
wheel3x2          = Motor(Ports.PORT2, GearSetting.RATIO_18_1, True)
catchError2x2Red  = Optical(Ports.PORT7)
catchError2x2Blue = Optical(Ports.PORT9)
catchError3x2Red  = Optical(Ports.PORT8)
catchError3x2Blue = Optical(Ports.PORT10)
startBumper       = Bumper(brain.three_wire_port.b)

wait(30, MSEC)

treadTopVolt  = 2.5
treadBotVolt  = 1
wheelVolt     = 1.5
lightSortPct  = 100
lightCatchPct = 25
loopWait      = 0.15
timeoutSec    = 120
debounceMs    = 50
stopHoldMs    = 500

errorCountRed  = 0
errorCountBlue = 0


def waitForRelease():
    while startBumper.pressing():
        wait(10, MSEC)
    wait(debounceMs, MSEC)


def isDebounced():
    if not startBumper.pressing():
        return False
    wait(debounceMs, MSEC)
    return startBumper.pressing()


def isStopHeld():
    if not startBumper.pressing():
        return False
    wait(stopHoldMs, MSEC)
    return startBumper.pressing()


def updateScreen():
    brain.screen.clear_screen()
    brain.screen.set_cursor(1, 1)
    brain.screen.print("Incorrect Red:  " + str(errorCountRed))
    brain.screen.next_row()
    brain.screen.print("Incorrect Blue: " + str(errorCountBlue))
    brain.screen.next_row()
    brain.screen.print("Total Errors:   " + str(errorCountRed + errorCountBlue))


def lightsOff():
    optical2x2.set_light(LedStateType.OFF)
    optical3x2.set_light(LedStateType.OFF)
    catchError2x2Blue.set_light(LedStateType.OFF)
    catchError2x2Red.set_light(LedStateType.OFF)
    catchError3x2Blue.set_light(LedStateType.OFF)
    catchError3x2Red.set_light(LedStateType.OFF)


def stopAll():
    bottomTread.stop()
    topTread.stop()
    wheel2x2.stop()
    wheel3x2.stop()


def whenStarted():
    global errorCountRed, errorCountBlue

    while True:
        if isDebounced():
            waitForRelease()

            errorCountRed  = 0
            errorCountBlue = 0
            brain.screen.clear_screen()

            topTread.spin(FORWARD, treadTopVolt, VOLT)
            bottomTread.spin(FORWARD, treadBotVolt, VOLT)
            wheel2x2.spin(FORWARD, wheelVolt, VOLT)
            wheel3x2.spin(FORWARD, wheelVolt, VOLT)

            optical2x2.set_light_power(lightSortPct, PERCENT)
            optical3x2.set_light_power(lightSortPct, PERCENT)
            catchError2x2Blue.set_light_power(lightCatchPct, PERCENT)
            catchError2x2Red.set_light_power(lightCatchPct, PERCENT)
            catchError3x2Blue.set_light_power(lightCatchPct, PERCENT)
            catchError3x2Red.set_light_power(lightCatchPct, PERCENT)

            prev2x2BlueRed = False
            prev3x2BlueRed = False
            prev2x2RedBlue = False
            prev3x2RedBlue = False

            startTime = brain.timer.time(SECONDS)

            while True:
                if isStopHeld():
                    waitForRelease()
                    break

                color2x2Blue = catchError2x2Blue.color()
                color3x2Blue = catchError3x2Blue.color()
                color2x2Red  = catchError2x2Red.color()
                color3x2Red  = catchError3x2Red.color()

                cur2x2BlueRed = (color2x2Blue == Color.RED)
                cur3x2BlueRed = (color3x2Blue == Color.RED)
                cur2x2RedBlue = (color2x2Red  == Color.BLUE)
                cur3x2RedBlue = (color3x2Red  == Color.BLUE)

                if cur2x2BlueRed and not prev2x2BlueRed:
                    errorCountRed += 1
                if cur3x2BlueRed and not prev3x2BlueRed:
                    errorCountRed += 1
                if cur2x2RedBlue and not prev2x2RedBlue:
                    errorCountBlue += 1
                if cur3x2RedBlue and not prev3x2RedBlue:
                    errorCountBlue += 1

                prev2x2BlueRed = cur2x2BlueRed
                prev3x2BlueRed = cur3x2BlueRed
                prev2x2RedBlue = cur2x2RedBlue
                prev3x2RedBlue = cur3x2RedBlue

                if optical2x2.color() == Color.RED:
                    wheel2x2.spin(FORWARD, wheelVolt, VOLT)
                elif optical2x2.color() == Color.BLUE:
                    wheel2x2.spin(REVERSE, wheelVolt, VOLT)

                if optical3x2.color() == Color.RED:
                    wheel3x2.spin(FORWARD, 2, VOLT)
                elif optical3x2.color() == Color.BLUE:
                    wheel3x2.spin(REVERSE, 2, VOLT)

                wait(loopWait, SECONDS)

            stopAll()
            lightsOff()
            updateScreen()

        wait(10, MSEC)

whenStarted()
