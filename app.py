import planthub
from threading import Thread, Event
from queue import Queue

# ONE TIME TASKS

#setup all of the parts
planthub.setup_humidity()
planthub.setup_photosensor()
planthub.setup_soil()
planthub.setup_display()
planthub.setup_buttons()

state = planthub.state()
screen = 0
next_screen = 1 #this means that the display is off

e = Event()

# Tasks that always run
# detect the button press
def detect_buttons():
    while True:
        if planthub.detect_push():
	    e.set()
            break

# Tasks that are triggered by other events (button press)
# turn on/off
def turn_on_off():
    global state, screen, next_screen
    print(state)
    e.wait()
    while True:
        if state == 1:
            if screen == 1:
                planthub.turn_off_display()
                next_screen = 1
            elif screen == 0:
                planthub.turn_on_display()
                next_screen = 2

# switch through screens
def switch_screens():
    global state, next_screen
    e.wait()
    if state == 2: # means the next page button was pressed
        if next_screen == 1:
            planthub.write_text("Light: ", planthub.output_photosensor())
            next_screen = 2
            print("screen=1")
        elif next_screen == 2:
            planthub.write_text("Humidity: ", planthub.read_humidity())
            next_screen = 3
            print("screen=2")
        elif next_screen == 4:
            planthub.write_text("Temp: ", planthub.soil_temp())
            next_screen = 5
            print("screen=3")
        elif next_screen == 5:
            planthub.write_text("Soil: ", planthub.soil_moisture())
            next_screen = 1 # back to the light level
            print("screen=4")

t1 = Thread(target=detect_buttons)
t1.start()
t2 = Thread(target=turn_on_off)
t2.start()
t3 = Thread(target=switch_screens)
t3.start()
t1.join()
t2.join()
t3.join()
