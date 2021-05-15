import Adafruit_DHT
import sys
import RPi.GPIO as GPIO
import time

from board import SCL, SDA
import busio

from adafruit_seesaw.seesaw import Seesaw

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

def info():
    '''Prints a basic library description'''
    print("Software library for the Plant Hub project.")


'''Humidity Sensor (DHT11) - Returns two values'''
sensor = 0
pin = 0

def setup_humidity():
    #print("This sets up the humidity sensor")
    global sensor
    global pin
    sensor = Adafruit_DHT.DHT11
    pin = 4

def read_humidity_temp():
    #print("This reads humidity and temperature values from the humidity sensor")
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
    return humidity, temperature

def print_humidity():
    humidity, temperature = read_humidity_temp()
#    print("Humidity={0.1f}%".format(humidity))
    return str(humidity)

def print_temp():
    humidity, temperature = read_humidity_temp()
#    form = ("Temp={0.1f}*C%".format(temperature))
    return str(temp)

'''Photosensor (DV-P8103)'''
# globalize the gpio pins to use in different functions
GPIO_A = 0
GPIO_B = 0

def setup_photosensor():
    global GPIO_A
    global GPIO_B

    GPIO.setmode(GPIO.BCM) #uses BCM pin numbering
    GPIO_A = 17
    GPIO_B = 27

def read_light_level():
    global GPIO_A
    global GPIO_B
    start = 0
    end = 0

# let capacitor discharge
    GPIO.setup(GPIO_A, GPIO.IN) #setting A as input will disconnect R_charge & R_var
    GPIO.setup(GPIO_B, GPIO.OUT)
    GPIO.output(GPIO_B, GPIO.LOW)
    time.sleep(1)

# charge through variable resistor
    GPIO.setup(GPIO_B,GPIO.IN)
    GPIO.setup(GPIO_A, GPIO.OUT)
    start = time.time()
    GPIO.output(GPIO_A, GPIO.HIGH)
    GPIO.wait_for_edge(GPIO_B, GPIO.RISING, timeout=2000)
    end = time.time()

    return start, end
    #print("This reads the light level from the photosensor")

def output_photosensor():
    start, end = read_light_level()
    return ("%f seconds, %f us" % (end-start, 1000000*(end-start)))
    #print("This outputs the light level from the photosensor")


'''STEMMA Soil Sensor'''
i2c_bus = busio.I2C(SCL,SDA)
ss = Seesaw(i2c_bus, addr=0x36)

def setup_soil():
    i2c_bus = busio.I2C(SCL,SDA)
    ss = Seesaw(i2c_bus, addr=0x36)
    #print("This sets up the STEMMA Soil Sensor")

def soil_moisture():
    moisture = ss.moisture_read()
    return moisture
    #print("This reads the moisture values from the soil sensor")

def soil_temp():
    temp = ss.get_temp()
    return temp
    #print("This reads the temperature values from the soil sensor")


'''LCD Display'''
# GPIO pin to LCD pin mapping
LCD_RS = 0
LCD_E = 0
LCD_D4 = 0
LCD_D5 = 0
LCD_D6 = 0
LCD_D7 = 0

# Define state of RS pin in character and command mode
LCD_CHR = GPIO.HIGH # High in data (character) mode
LCD_CMD = GPIO.LOW # Low in instruction (command) mode

#Important commands
LCD_CLEAR = 0
LCD_D_OFF = 0
LCD_4BIT1 = 0
LCD_4BIT2 = 0
LCD_ON_NC = 0
LCD_ENTRY = 0

# Timing constants
E_PULSE = 0.0005
E_DELAY = 0.0005

def char_to_arr(c):
    return [int(b) for b in format(ord(c), '08b')]

def setup_display():
    global LCD_RS, LCD_E, LCD_D4, LCD_D5, LCD_D6, LCD_D7, LCD_CHR, LCD_CMD, LCD_CLEAR, LCD_D_OFF, LCD_4BIT1, LCD_4BIT2, LCD_ON_NC, LCD_ENTRY, E_PULSE, E_DELAY
    GPIO.setmode(GPIO.BCM)

# GPIO pin to LCD pin mapping
    LCD_RS = 6
    LCD_E = 5
    LCD_D4 = 25
    LCD_D5 = 24
    LCD_D6 = 23
    LCD_D7 = 22

# Define state of RS pin in character and command mode
    LCD_CHR = GPIO.HIGH # High in data (character) mode
    LCD_CMD = GPIO.LOW # Low in instruction (command) mode

#Important commands
    LCD_CLEAR = [0,0,0,0,0,0,0,1]
    LCD_D_OFF = [0,0,0,0,1,0,0,0]
    LCD_4BIT1 = [0,0,1,1,0,0,1,1]
    LCD_4BIT2 = [0,0,1,1,0,0,1,0]
    LCD_ON_NC = [0,0,0,0,1,1,0,0]
    LCD_ENTRY = [0,0,0,0,0,1,1,0]

# Timing constants
    E_PULSE = 0.0005
    E_DELAY = 0.0005

    #print("This sets up the LCD Display")
    pins = [LCD_RS, LCD_E, LCD_D7, LCD_D6, LCD_D5, LCD_D4]

    for p in zip(pins):
        GPIO.setup(p, GPIO.OUT)

    write_arr_4_bit(LCD_4BIT1, LCD_CMD)
    write_arr_4_bit(LCD_4BIT2, LCD_CMD)
    write_arr_4_bit(LCD_ON_NC, LCD_CMD)
    write_arr_4_bit(LCD_ENTRY, LCD_CMD)
    write_arr_4_bit(LCD_CLEAR, LCD_CMD)

def write_text(phrase):
    for c in phrase:
        write_arr_4_bit(char_to_arr(c), LCD_CHR)

def turn_on_display():
    setup_display()
    #print("This turns on the LCD Display")

def turn_off_display():
    write_arr_4_bit(LCD_CLEAR, LCD_CMD) #clear display
    write_arr_4_bit(LCD_D_OFF, LCD_CMD) # turns display off 0000 1000
    GPIO.cleanup()

def clear_display():
    write_arr_4_bit(LCD_CLEAR, LCD_CMD) #clear display

def write_arr_4_bit(bits, mode, debug=True):
    global LCD_RS
    #print("This writes texts to the LCD Display")
    pins = [LCD_D7, LCD_D6, LCD_D5, LCD_D4]

    GPIO.output(LCD_RS, mode) #RS - command or character mode

    # set most significant bits (high bits) on data lines
    for p, b in zip(pins, bits[:4]):
        GPIO.setup(p, GPIO.OUT)
        GPIO.output(p,b)

    # pulse clock
    time.sleep(E_DELAY)
    GPIO.output(LCD_E, GPIO.HIGH)
    time.sleep(E_PULSE)
    GPIO.output(LCD_E, GPIO.LOW)
    time.sleep(E_DELAY)

    # set least significant bits on data lines
    for p, b in zip(pins, bits[4:]):
        GPIO.setup(p, GPIO.OUT)
        GPIO.output(p, b)

    # pulse clock
    time.sleep(E_DELAY)
    GPIO.output(LCD_E, GPIO.HIGH)
    time.sleep(E_PULSE)
    GPIO.output(LCD_E, GPIO.LOW)
    time.sleep(E_DELAY)

    # reset pins to 0
    for p in pins:
        GPIO.output(p, GPIO.LOW)



'''Buttons'''
#globalize the buttons first
b1 = 16
b2 = 26
state1 = 0

def setup_buttons():
    global b1, b2
    #print("This sets up the buttons")
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)

    GPIO.setup(b1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(b2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

def detect_push():
    global b1, b2
    #print("This detects button pushes")
    GPIO.add_event_detect(b1, GPIO.FALLING, callback=lambda x: detect_interrupt(b1))
    GPIO.add_event_detect(b2, GPIO.FALLING, callback=lambda x: detect_interrupt(b2))

def detect_interrupt(button):
    global state1
    state1 = 0
    if button == 16:
       state1 = 1
       print("on/off")
    elif button == 26:
       state1 = 2
       print("switch screens")

def state():
    global state1
    return state1
