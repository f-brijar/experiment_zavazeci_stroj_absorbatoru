from guizero import App, Window, PushButton, Drawing
from RPi import GPIO
import threading, time, sys, spidev
import clickers, pins



GPIO.setmode(GPIO.BOARD)
GPIO.setup(pins.switch_1_state, GPIO.IN)
GPIO.setup(pins.switch_2_state, GPIO.IN)
GPIO.setup(pins.switch_3_state, GPIO.IN)
GPIO.setup(pins.switch_4_state, GPIO.IN)
GPIO.setup(pins.switch_6_state, GPIO.IN)
GPIO.setup(pins.relay_1, GPIO.OUT)
GPIO.setup(pins.relay_2, GPIO.OUT)
GPIO.setup(pins.relay_3, GPIO.OUT)
GPIO.setup(pins.relay_4, GPIO.OUT)
GPIO.setup(pins.relay_5, GPIO.OUT)
GPIO.setup(pins.relay_6, GPIO.OUT)

switch_states = [0,0,0,0,0,0]
stop_threads  = False

def thread_switches(
        switch_1_state,
        switch_2_state,
        switch_3_state,
        switch_4_state,
        switch_5_state,
        switch_6_state
    ):
    while True:
        sw1_state = GPIO.input(pins.switch_1_state)
        sw2_state = GPIO.input(pins.switch_2_state)
        sw3_state = GPIO.input(pins.switch_3_state)
        sw4_state = GPIO.input(pins.switch_4_state)
        sw5_state = GPIO.input(pins.switch_5_state)
        sw6_state = GPIO.input(pins.switch_6_state)
        global switch_states
        switch_states = (sw1_state, sw2_state, sw3_state, sw4_state, sw5_state, sw6_state)
        if (sw1_state == False):
            GPIO.output(pins.relay_1, 0)
        if (sw2_state == False):
            GPIO.output(pins.relay_2, 0)
        if (sw3_state == False):
            GPIO.output(pins.relay_3, 0)
        if (sw4_state == False):
            GPIO.output(pins.relay_4, 0)
        if (sw5_state == False):
            GPIO.output(pins.relay_5, 0)
        if (sw6_state == False):
            GPIO.output(pins.relay_6, 0)
        global stop_threads
        if stop_threads:
            break
        else:
            time.sleep(0.25)

thr_switches = threading.Thread(
    target=thread_switches,
    args = (pins.switch_1_state,pins.switch_2_state,pins.switch_3_state,pins.switch_4_state,pins.switch_5_state,pins.switch_6_state)
)
thr_switches.start()

def switch_on():
    print("switch_on")
    GPIO.output(pins.relay_1, 1)

def switch_off():
    print("switch_off")
    GPIO.output(pins.relay_1, 0)


def on_close():
    elements_pump[0].cancel(drawing_update_pump)
    elements_valve[0].cancel(drawing_update_valve)
    elements_lights[0].cancel(drawing_update_lights)
    elements_outlet_1[0].cancel(drawing_update_outlet_1)
    elements_outlet_2[0].cancel(drawing_update_outlet_2)
    elements_outlet_3[0].cancel(drawing_update_outlet_3)
    global stop_threads
    stop_threads = True
    thr_switches.join()
    GPIO.output(pins.relay_1, 0)
    GPIO.cleanup()
    app.destroy()

app = App("Experiment", layout="grid")
app.when_closed  = on_close

def drawing_update_pump(sw_number):
    global switch_states
    global elements_pump
    elements_pump[0].delete(elements_pump[1])
    elements_pump[0].delete(elements_pump[2])
    elements_pump[0].delete(elements_pump[3])
    if (switch_states[sw_number-1] == 1):
        if (GPIO.input(pins.relay_1) == True):
            elements_pump[1] = elements_pump[0].rectangle(30, 10, 110, 90, color="green")
            elements_pump[2] = elements_pump[0].rectangle(35, 15, 105, 85, color="white")
            elements_pump[3] = elements_pump[0].image(30, 10, "./icons/pump_on.png")
        else:
            elements_pump[1] = elements_pump[0].rectangle(30, 10, 110, 90, color="red")
            elements_pump[2] = elements_pump[0].rectangle(35, 15, 105, 85, color="white")
            elements_pump[3] = elements_pump[0].image(30, 10, "./icons/pump_off.png")            
    else:
        elements_pump[1] = elements_pump[0].rectangle(30, 10, 110, 90, color="black")
        elements_pump[2] = elements_pump[0].rectangle(35, 15, 105, 85, color="white")
        elements_pump[3] = elements_pump[0].image(30, 10, "./icons/pump_off.png")

def drawing_update_valve(sw_number):
    global switch_states
    global elements_valve
    elements_valve[0].delete(elements_valve[1])
    elements_valve[0].delete(elements_valve[2])
    elements_valve[0].delete(elements_valve[3])
    if (switch_states[sw_number-1] == 1):
        if (GPIO.input(pins.relay_2) == True):
            elements_valve[1] = elements_valve[0].rectangle(30, 10, 110, 90, color="green")
            elements_valve[2] = elements_valve[0].rectangle(35, 15, 105, 85, color="white")
            elements_valve[3] = elements_valve[0].image(30, 10, "./icons/valve_on.png")
        else:
            elements_valve[1] = elements_valve[0].rectangle(30, 10, 110, 90, color="red")
            elements_valve[2] = elements_valve[0].rectangle(35, 15, 105, 85, color="white")
            elements_valve[3] = elements_valve[0].image(30, 10, "./icons/valve_off.png")
    else:
        elements_valve[1] = elements_valve[0].rectangle(30, 10, 110, 90, color="black")
        elements_valve[2] = elements_valve[0].rectangle(35, 15, 105, 85, color="white")
        elements_valve[3] = elements_valve[0].image(30, 10, "./icons/valve_off.png")

def drawing_update_lights(sw_number):
    global switch_states
    global elements_lights
    elements_lights[0].delete(elements_lights[1])
    elements_lights[0].delete(elements_lights[2])
    elements_lights[0].delete(elements_lights[3])
    if (switch_states[sw_number-1] == 1):
        if (GPIO.input(pins.relay_3) == True):
            elements_lights[1] = elements_lights[0].rectangle(30, 10, 110, 90, color="green")
            elements_lights[2] = elements_lights[0].rectangle(35, 15, 105, 85, color="white")
            elements_lights[3] = elements_lights[0].image(30, 10, "./icons/lights_on.png")
        else:
            elements_lights[1] = elements_lights[0].rectangle(30, 10, 110, 90, color="red")
            elements_lights[2] = elements_lights[0].rectangle(35, 15, 105, 85, color="white")
            elements_lights[3] = elements_lights[0].image(30, 10, "./icons/lights_off.png")
    else:
        elements_lights[1] = elements_lights[0].rectangle(30, 10, 110, 90, color="black")
        elements_lights[2] = elements_lights[0].rectangle(35, 15, 105, 85, color="white")
        elements_lights[3] = elements_lights[0].image(30, 10, "./icons/lights_off.png")

def drawing_update_outlet_1(sw_number):
    global switch_states
    global elements_outlet_1
    elements_outlet_1[0].delete(elements_outlet_1[1])
    elements_outlet_1[0].delete(elements_outlet_1[2])
    elements_outlet_1[0].delete(elements_outlet_1[3])
    if (switch_states[sw_number-1] == 1):
        if (GPIO.input(pins.relay_4) == True):
            elements_outlet_1[1] = elements_outlet_1[0].rectangle(30, 10, 110, 90, color="green")
            elements_outlet_1[2] = elements_outlet_1[0].rectangle(35, 15, 105, 85, color="white")
            elements_outlet_1[3] = elements_outlet_1[0].image(30, 10, "./icons/switch_on.png")
        else:
            elements_outlet_1[1] = elements_outlet_1[0].rectangle(30, 10, 110, 90, color="red")
            elements_outlet_1[2] = elements_outlet_1[0].rectangle(35, 15, 105, 85, color="white")
            elements_outlet_1[3] = elements_outlet_1[0].image(30, 10, "./icons/switch_off.png")
    else:
        elements_outlet_1[1] = elements_outlet_1[0].rectangle(30, 10, 110, 90, color="black")
        elements_outlet_1[2] = elements_outlet_1[0].rectangle(35, 15, 105, 85, color="white")
        elements_outlet_1[3] = elements_outlet_1[0].image(30, 10, "./icons/switch_off.png")

def drawing_update_outlet_2(sw_number):
    global switch_states
    global elements_outlet_2
    elements_outlet_2[0].delete(elements_outlet_2[1])
    elements_outlet_2[0].delete(elements_outlet_2[2])
    elements_outlet_2[0].delete(elements_outlet_2[3])
    if (switch_states[sw_number-1] == 1):
        if (GPIO.input(pins.relay_5) == True):
            elements_outlet_2[1] = elements_outlet_2[0].rectangle(30, 10, 110, 90, color="green")
            elements_outlet_2[2] = elements_outlet_2[0].rectangle(35, 15, 105, 85, color="white")
            elements_outlet_2[3] = elements_outlet_2[0].image(30, 10, "./icons/switch_on.png")
        else:
            elements_outlet_2[1] = elements_outlet_2[0].rectangle(30, 10, 110, 90, color="red")
            elements_outlet_2[2] = elements_outlet_2[0].rectangle(35, 15, 105, 85, color="white")
            elements_outlet_2[3] = elements_outlet_2[0].image(30, 10, "./icons/switch_off.png")
    else:
        elements_outlet_2[1] = elements_outlet_2[0].rectangle(30, 10, 110, 90, color="black")
        elements_outlet_2[2] = elements_outlet_2[0].rectangle(35, 15, 105, 85, color="white")
        elements_outlet_2[3] = elements_outlet_2[0].image(30, 10, "./icons/switch_off.png")

def drawing_update_outlet_3(sw_number):
    global switch_states
    global elements_outlet_3
    elements_outlet_3[0].delete(elements_outlet_3[1])
    elements_outlet_3[0].delete(elements_outlet_3[2])
    elements_outlet_3[0].delete(elements_outlet_3[3])
    if (switch_states[sw_number-1] == 1):
        if (GPIO.input(pins.relay_6) == True):
            elements_outlet_3[1] = elements_outlet_3[0].rectangle(30, 10, 110, 90, color="green")
            elements_outlet_3[2] = elements_outlet_3[0].rectangle(35, 15, 105, 85, color="white")
            elements_outlet_3[3] = elements_outlet_3[0].image(30, 10, "./icons/switch_on.png")
        else:
            elements_outlet_3[1] = elements_outlet_3[0].rectangle(30, 10, 110, 90, color="red")
            elements_outlet_3[2] = elements_outlet_3[0].rectangle(35, 15, 105, 85, color="white")
            elements_outlet_3[3] = elements_outlet_3[0].image(30, 10, "./icons/switch_off.png")
    else:
        elements_outlet_3[1] = elements_outlet_3[0].rectangle(30, 10, 110, 90, color="black")
        elements_outlet_3[2] = elements_outlet_3[0].rectangle(35, 15, 105, 85, color="white")
        elements_outlet_3[3] = elements_outlet_3[0].image(30, 10, "./icons/switch_off.png")

elements_pump     = []
elements_valve    = []
elements_lights   = []
elements_outlet_1 = []
elements_outlet_2 = []
elements_outlet_3 = []

elements_pump.append( Drawing(app, grid=[1,1,1,1], width=140, height=100) )
elements_valve.append( Drawing(app, grid=[2,1,1,1], width=140, height=100) )
elements_lights.append( Drawing(app, grid=[3,1,1,1], width=140, height=100) )
elements_outlet_1.append( Drawing(app, grid=[4,1,1,1], width=140, height=100) )
elements_outlet_2.append( Drawing(app, grid=[5,1,1,1], width=140, height=100) )
elements_outlet_3.append( Drawing(app, grid=[6,1,1,1], width=140, height=100) )

elements_pump.append( elements_pump[0].rectangle(30, 10, 110, 90, color="black") )
elements_valve.append( elements_valve[0].rectangle(30, 10, 110, 90, color="black") )
elements_lights.append( elements_lights[0].rectangle(30, 10, 90, 110, color="black") )
elements_outlet_1.append( elements_outlet_1[0].rectangle(30, 10, 110, 90, color="black") )
elements_outlet_2.append( elements_outlet_2[0].rectangle(30, 10, 110, 90, color="black") )
elements_outlet_3.append( elements_outlet_3[0].rectangle(30, 10, 110, 90, color="black") )

elements_pump.append( elements_pump[0].rectangle(35, 15, 105, 85, color="white") )
elements_valve.append( elements_valve[0].rectangle(35, 15, 105, 85, color="white") )
elements_lights.append( elements_lights[0].rectangle(35, 15, 105, 85, color="white") )
elements_outlet_1.append( elements_outlet_1[0].rectangle(35, 15, 105, 85, color="white") )
elements_outlet_2.append( elements_outlet_2[0].rectangle(35, 15, 105, 85, color="white") )
elements_outlet_3.append( elements_outlet_3[0].rectangle(35, 15, 105, 85, color="white") )

elements_pump.append( elements_pump[0].image(35, 15, "./icons/pump_off.png") )
elements_valve.append( elements_valve[0].image(35, 15, "./icons/valve_off.png") )
elements_lights.append( elements_lights[0].image(35, 15, "./icons/lights_off.png") )
elements_outlet_1.append( elements_outlet_1[0].image(35, 15, "./icons/switch_off.png") )
elements_outlet_2.append( elements_outlet_2[0].image(35, 15, "./icons/switch_off.png") )
elements_outlet_3.append( elements_outlet_3[0].image(35, 15, "./icons/switch_off.png") )

elements_pump[0].repeat(100, drawing_update_pump, (1,))
elements_valve[0].repeat(100, drawing_update_valve, (2,))
elements_lights[0].repeat(100, drawing_update_lights, (3,))
elements_outlet_1[0].repeat(100, drawing_update_outlet_1, (4,))
elements_outlet_2[0].repeat(100, drawing_update_outlet_2, (5,))
elements_outlet_3[0].repeat(100, drawing_update_outlet_3, (6,))

elements_pump[0].when_clicked = clickers.click_pump
elements_valve[0].when_clicked = clickers.click_valve
elements_lights[0].when_clicked = clickers.click_lights
elements_outlet_1[0].when_clicked = clickers.click_outlet_1
elements_outlet_2[0].when_clicked = clickers.click_outlet_2
elements_outlet_3[0].when_clicked = clickers.click_outlet_3


#SPI
spi = spidev.SpiDev()
bus = 0 # Pi only has SPI bus 0 available
dev = 1 # Chip selectpin. Set to 0 or 1, depending on the connections
spi.open(bus, dev)
spi.max_speed_hz = 500000
spi.mode         = 0

