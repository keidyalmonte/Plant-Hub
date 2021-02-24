import planthub

print("You are now testing the PlantHub Software Library")

print("")

print("planthub.info()")
planthub.info()

print("")

print("Humidity Sensor DHT11 TEST")
print("planthub.setup_humidity()")
planthub.setup_humidity()
print("planthub.read_humidity()")
planthub.read_humidity()
print("planthub.read_temp()")
planthub.read_temp()

print("")

print("Photosensor DV-P8103 TEST")
print("planthub.setup_photosensor()")
planthub.setup_photosensor()
print("planthub.read_light_level()")
planthub.read_light_level()
print("planthub.output_photosensor()")
planthub.output_photosensor()

print("")

print("STEMMA Soil Sensor TEST")
print("planthub.setup_soil()")
planthub.setup_soil()
print("planthub.soil_moisture()")
planthub.soil_moisture()
print("planthub.soil_temp()")
planthub.soil_temp()

print("")

print("LCD Display TEST")
print("planthub.setup_display()")
planthub.setup_display()
print("planthub.turn_on_display()")
planthub.turn_on_display()
print("planthub.turn_off_display()")
planthub.turn_off_display()
print("planthub.write_text()")
planthub.write_text()

print("")

print("Potentiometer TEST")
print("planthub.setup_potentiometer()")
planthub.setup_potentiometer()
print("planthub.set_resistance_p()")
planthub.set_resistance_p()

print("")

print("Buttons TEST")
print("planthub.setup_buttons()")
planthub.setup_buttons()
print("planthub.detect_push()")
planthub.detect_push()
print("planthub.detect_interrupt()")
planthub.detect_interrupt()

print("")
print("You are now done testing")
