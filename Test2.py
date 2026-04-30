from vex import * #import vex library
import urandom    #import urandom library
import math       #import math library

brain=Brain()     #Define the brain and set it to the brain variable

bottomTread = Motor(Ports.PORT2, GearSetting.RATIO_18_1, True)  #Define bottom tread motor
topTread = Motor(Ports.PORT1, GearSetting.RATIO_18_1, True)
optical2x2 = Optical(Ports.PORT4)                               #Define optical sensor used for
wheel2x2 = Motor(Ports.PORT3, GearSetting.RATIO_18_1, True)
catchError2x2Red = Optical(Ports.PORT7)
catchError2x2Blue = Optical(Ports.PORT9)
wheel3x2 = Motor(Ports.PORT5, GearSetting.RATIO_18_1, True)
optical3x2 = Optical(Ports.PORT6)
catchError3x2Red = Optical(Ports.PORT8)
catchError3x2Blue = Optical(Ports.PORT10)
startBumper = Bumper(brain.three_wire_port.b)

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
    print("033[2J")
    
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
            topTread.spin(FORWARD, 2.5, VOLT)
            bottomTread.spin(FORWARD, 1.2, VOLT)
            wheel2x2.spin(FORWARD, 1.5, VOLT)
            wheel3x2.spin(FORWARD, 1.5, VOLT)
            optical2x2.set_light_power(100, PERCENT)
            optical3x2.set_light_power(100, PERCENT)
            catchError3x2Blue.set_light_power(25, PERCENT)
            catchError3x2Red.set_light_power(25, PERCENT)
            catchError2x2Red.set_light_power(25, PERCENT)
            catchError2x2Blue.set_light_power(25, PERCENT)
            while (True):                
                if (catchError2x2Blue.color() == Color.BLUE):
                    blueCount += 1
                elif (catchError2x2Blue.color() == Color.RED):
                    errorCountRed += 1
                else:
                    wait(0.001, SECONDS)
                            
                if (catchError3x2Blue.color() == Color.BLUE):
                    blueCount += 1
                elif (catchError3x2Blue.color() == Color.RED):
                    errorCountRed += 1
                else:
                    wait(0.001, SECONDS)
                                
                if (catchError2x2Red.color() == Color.RED):
                    redCount += 1
                elif (catchError2x2Red.color() == Color.BLUE):
                    errorCountBlue += 1
                else:
                    wait(0.001, SECONDS)
                    
                if (catchError3x2Red.color() == Color.RED):
                    redCount += 1
                elif (catchError3x2Red.color() == Color.BLUE):
                    errorCountBlue += 1                
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
                    break

                wait(0.15, SECONDS)

            bottomTread.stop()
            topTread.stop()
            wheel2x2.stop()
            wheel3x2.stop()
            optical2x2.set_light(LedStateType.OFF)
            optical3x2.set_light(LedStateType.OFF)
            catchError3x2Blue.set_light(LedStateType.OFF)
            catchError3x2Red.set_light(LedStateType.OFF)
            catchError2x2Blue.set_light(LedStateType.OFF)
            catchError2x2Red.set_light(LedStateType.OFF)
            errorCountRed += (4 - redCount)
            errorCountBlue += (6 - blueCount)
            brain.screen.set_cursor(1, 1)
            brain.screen.print("Correct Red Blocks: " + str(redCount))
            brain.screen.next_row()
            brain.screen.print("Incorrect Red Blocks: " + str(errorCountRed))
            brain.screen.next_row()
            brain.screen.print("Correct Blue Blocks: " + str(blueCount))
            brain.screen.next_row()
            brain.screen.print("Incorrect Blue Blocks: " + str(errorCountBlue))
            brain.screen.next_row()
        wait(0.1, SECONDS)

when_started1()
