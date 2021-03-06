import planthub

print("You are now testing the PlantHub Software Library")

print("")

print("planthub.info()")
planthub.info()

print("")
print("Now testing each individual part. If you would like to skip testing on a specific part, use '^C' to enable keyboard interrupt.")

print("Humidity Sensor DHT11 TEST")
try:
    print("planthub.setup_humidity()")
    planthub.setup_humidity()
    print("planthub.read_humidity_temp()")
    planthub.read_humidity_temp()
    print("planthub.print_values")
    planthub.print_values()
except KeyboardInterrupt:
    print("")

print("")

print("Photosensor DV-P8103 TEST")
try:
    print("planthub.setup_photosensor()")
    planthub.setup_photosensor()
    print("planthub.read_light_level()")
    planthub.read_light_level()
    print("planthub.output_photosensor()")
    planthub.output_photosensor()
except KeyboardInterrupt:
    print("")

print("")

print("STEMMA Soil Sensor TEST")
try:
    print("planthub.setup_soil()")
    planthub.setup_soil()
    print("planthub.soil_moisture()")
    planthub.soil_moisture()
    print("planthub.soil_temp()")
    planthub.soil_temp()
except KeyboardInterrupt:
    print("")

print("")
print("LCD Display TEST")
print("planthub.setup_display()")
planthub.setup_display()
print("planthub.turn_on_display()")
planthub.turn_on_display()
planthub.write_text("Hello World")
#planthub.turn_off_display()
print("planthub.write_text()")
#print("planthub.turn_off_display()")
print("")

print("Buttons TEST")
print("planthub.setup_buttons()")
planthub.setup_buttons()
print("planthub.detect_push()")
planthub.detect_push()
#print("planthub.detect_interrupt()")
#planthub.detect_interrupt()

print("")
print("You are now done testing")
