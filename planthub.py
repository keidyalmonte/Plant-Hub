import sys
import Adafruit_DHT
import RPi.GPIO as GPIO
import time

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

def print_values():
    humidity, temperature = read_humidity_temp()
    print("Temp={0:0.1f}*C Humidity={1:0.1f}%".format(temperature,humidity))


'''Photosensor (DV-P8103)'''
# globalize the gpio pins to use in different functions
GPIO_A = 0
GPIO_B = 0

def setup_photosensor():
    global GPIO_A
    global GPIO_B

    GPIO.setmode(GPIO.BCM) #uses BCM pin numbering
    GPIO_A = 27
    GPIO_B = 22

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
    print("%f seconds, %f us" % (end-start, 1000000*(end-start)))
    #print("This outputs the light level from the photosensor")


'''STEMMA Soil Sensor'''
def setup_soil():
    print("This sets up the STEMMA Soil Sensor")

def soil_moisture():
    print("This reads the moisture values from the soil sensor")

def soil_temp():
    print("This reads the temperature values from the soil sensor")


'''LCD Display'''
def setup_display():
    print("This sets up the LCD Display")

def turn_on_display():
    print("This turns on the LCD Display")

def turn_off_display():
    print("This turns off the LCD Display")

def write_text():
    print("This writes texts to the LCD Display")


'''Potentiometer'''
def setup_potentiometer():
    print("This sets up the potentiometer")

def set_resistance_p():
    print("This sets the resistance for the potentiometer")


'''Buttons'''
def setup_buttons():
    print("This sets up the buttons")

def detect_push():
    print("This detects button pushes")

def detect_interrupt():
    print("This detects interrupts from the buttons")

