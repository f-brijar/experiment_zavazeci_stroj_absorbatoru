try:
    from RPi import GPIO
except ModuleNotFoundError:
    import sys
    import fake_rpi
    sys.modules['RPi'] = fake_rpi.RPi     # Fake RPi
    sys.modules['RPi.GPIO'] = fake_rpi.RPi.GPIO # Fake GPIO
    from RPi import GPIO
import pins


def click_pump():
    if (GPIO.input(pins.switch_1_state) == True):
        if (GPIO.input(pins.relay_1) == False):
            GPIO.output(pins.relay_1, 1)
        else:
            GPIO.output(pins.relay_1, 0)
    print("click_pump")

def click_valve():
    if (GPIO.input(pins.switch_2_state) == True):
        if (GPIO.input(pins.relay_2) == False):
            GPIO.output(pins.relay_2, 1)
        else:
            GPIO.output(pins.relay_2, 0)
    print("click_valve")

def click_lights():
    if (GPIO.input(pins.switch_3_state) == True):
        if (GPIO.input(pins.relay_3) == False):
            GPIO.output(pins.relay_3, 1)
        else:
            GPIO.output(pins.relay_3, 0)
    print("click_lights")

def click_outlet_1():
    if (GPIO.input(pins.switch_4_state) == True):
        if (GPIO.input(pins.relay_4) == False):
            GPIO.output(pins.relay_4, 1)
        else:
            GPIO.output(pins.relay_4, 0)
    print("click_outlet_1")

def click_outlet_2():
    if (GPIO.input(pins.switch_5_state) == True):
        if (GPIO.input(pins.relay_5) == False):
            GPIO.output(pins.relay_5, 1)
        else:
            GPIO.output(pins.relay_5, 0)
    print("click_outlet_2")

def click_outlet_3():
    if (GPIO.input(pins.switch_6_state) == True):
        if (GPIO.input(pins.relay_6) == False):
            GPIO.output(pins.relay_6, 1)
        else:
            GPIO.output(pins.relay_6, 0)
    print("click_outlet_3")
