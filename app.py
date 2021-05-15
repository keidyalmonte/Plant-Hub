import planthub
import time
from threading import Thread, Event
from queue import Queue
from time import sleep

# ONE TIME TASKS

#setup all of the parts
planthub.setup_humidity()
planthub.setup_photosensor()
planthub.setup_soil()
planthub.setup_display()
planthub.setup_buttons()

state = planthub.state()
print(state)
screen = 0
curr_screen = 0
next_screen = 1 #this means that the display is off

e = Event()

# Tasks that always run
# detect the button press
def detect_buttons():
    planthub.detect_push()

# Tasks that are triggered by other events (button press)
# turn on/off
def turn_on_off():
   global next_screen, curr_screen
   state = planthub.state()
   if state == 1:
      if ((next_screen == 2) & (curr_screen == 1)):
         print("turn off")
         planthub.turn_off_display()
         next_screen = 1
         curr_screen = 0
      elif ((next_screen == 1) & (curr_screen == 0)):
         print("turn on")
         planthub.turn_on_display()
         next_screen = 2
         curr_screen = 1
   state = 0

# switch through screens
def switch_screens():
    global next_screen
    state = planthub.state()
    print(state)
    if state == 2: # means the next page button was pressed
        if (curr_screen == 1) | (next_screen == 1):
            planthub.clear_display()
            light = planthub.output_photosensor()
            planthub.write_text("Light: " + light)
            next_screen = 2
            print("screen=1")
        elif (next_screen == 2):
            planthub.clear_display()
            humidity = planthub.print_humidity()
            planthub.write_text("Humidity:" + str(humidity))
            next_screen = 3
            print("screen=2")
        elif (next_screen == 3):
            planthub.clear_display()
            temp = planthub.print_temp()
            planthub.write_text("Temp:" + str(temp))
            next_screen = 4
            print("screen=3")
        elif (next_screen == 4):
            planthub.clear_display()
            soil_moisture = planthub.soil_moisture
            planthub.write_text("Moist:" + str(soil_moisture))
            next_screen = 1 # back to the light level
            print("screen=4")
        time.sleep(1)

detect_buttons()

while True:
#    t1 = Thread(target=detect_buttons)
#    t1.start()
    t2 = Thread(target=turn_on_off)
    t2.start()
    t3 = Thread(target=switch_screens)
    t3.start()
#    t1.join()
    t2.join()
    t3.join()
    time.sleep(1)
