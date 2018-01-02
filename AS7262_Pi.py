"""A set of Python functions to control the Sparkfun AS7262 Visible spectrometer on a Raspberry Pi.
The Default I2C address of the device is 0x49, tested with a Pi 3B."""

from smbus import SMBus
import time
import struct

bus = SMBus(1)

#Function to read a single virtual register
def read_reg(reg_to_read):

	#Check the DEVICE_STATUS_REG (0x00) until it indicates
	#that the write buffer is ready to be written to
	while True:
		status = bus.read_byte_data(0x49, 0x00)
		#Continue if the write buffer is ready
		if (status & 0b00000010) == 0:
			break
		#Else keep waiting
		else:
			pass
	#When the write buffer is ready, write the value of the register
	#you want to read from into the DEVICE_WRITE_REG (0x01)
	bus.write_byte_data(0x49, 0x01, reg_to_read)

	#Check the DEVICE_STATUS_REG (0x00) until it indicates
	#that the read buffer contains data
	while True:
		status = bus.read_byte_data(0x49, 0x00)
		#Continue if the read buffer is ready
		if (status & 0b00000001) == 0x01:
			break
		#Else keep waiting
		else:
			pass
	#When the read buffer is ready, read the value from the
	#DEVICE_READ_REG (0x02)
	value = bus.read_byte_data(0x49, 0x02)
	
	return value

#Function to write to a single virtual register
def write_reg(reg_to_write_to, command_to_write):
	#Check the DEVICE_STATUS_REG (0x00) until it indicates
	#that the write buffer is ready to be written to
	while True:
		status = bus.read_byte_data(0x49, 0x00)
		#Continue if the write buffer is ready
		if (status & 0b00000010) == 0:
			break
		#Else keep waiting
		else:
			pass
	#Send DEVICE_WRITE_REG (0x01) the address of the reg you want to write
	#into. Bit 7 must be 1 to indicate this will be followed by a value
	#to be written into that register, done by bitwise OR-ing the
	#destination register with 0x80
	bus.write_byte_data(0x49, 0x01, (reg_to_write_to | 0x80))
	
	#Check the DEVICE_STATUS_REG (0x00) until it indicates
	#that the write buffer is ready to be written to
	while True:
		status = bus.read_byte_data(0x49, 0x00)
		#Continue if write buffer is ready
		if (status & 0b00000010) == 0:
			break
		#Else keep waiting
		else:
			pass
	#When the write buffer is ready, send DEVCE_WRITE_REG (0x01) the
	#command to be written into the register sent previously
	bus.write_byte_data(0x49, 0x01, command_to_write)

#Function to take a single measurement and return the ROYGBV values
def take_single_measurement():
	#Put the device into single-shot mode
	set_measurement_mode(3)
	#Get and return the values
	readings = get_calibrated_values()
	return readings

#Function to get, process and return the calibrated ROYGBV values
def get_calibrated_values():
	#Wait for data to arrive into the data registers
	#by checking the DATA_RDY bit of the Control Setup reg
	#Return None if waiting for more than 10 seconds
	start = time.time()
	while True:
		state = read_reg(0x04)
		#If the data is ready then break to the next stage
		if (state & 0b00000010) == 0b00000010:
			break
		#Otherwise keep waiting, or quit if waited more than 10s
		else:
			if (time.time() >= (start + 10)):
				print("Error, no data available. Did you use set_measurement_mode() to tell the device to take a reading?")
				return
			else:
				pass
	#Read all of the calibrated results into colour_bytes[]
	colour_bytes = []
	for x in range (0x14, 0x2C):
		colour_bytes.append(read_reg(x))
	
	#Split the bytes by colour and place into colour specific lists 
	v = [colour_bytes[0], colour_bytes[1], colour_bytes[2],\
 colour_bytes[3]]
	b = [colour_bytes[4], colour_bytes[5], colour_bytes[6],\
 colour_bytes[7]]
	g = [colour_bytes[8], colour_bytes[9], colour_bytes[10],\
 colour_bytes[11]]
	y = [colour_bytes[12], colour_bytes[13], colour_bytes[14],\
 colour_bytes[15]]
	o = [colour_bytes[16], colour_bytes[17], colour_bytes[18],\
 colour_bytes[19]]
	r = [colour_bytes[20], colour_bytes[21], colour_bytes[22],\
 colour_bytes[23]]

	#Convert the values from IEEE 754 standard floats to Python floats,
	#place in calibrated_values list in the order [R,O,Y,G,B,V]
	calibrated_values = []
	calibrated_values.append(struct.unpack('>f', bytearray(r))[0])
	calibrated_values.append(struct.unpack('>f', bytearray(o))[0])
	calibrated_values.append(struct.unpack('>f', bytearray(y))[0])
	calibrated_values.append(struct.unpack('>f', bytearray(g))[0])
	calibrated_values.append(struct.unpack('>f', bytearray(b))[0])
	calibrated_values.append(struct.unpack('>f', bytearray(v))[0])

	return	calibrated_values

#Function to turn the main LED on, take single-shot measurements, 
# turn the main led off and return those measurements as a list in
# ROYGBV order (essentally take_measurements with main led on/off)
def take_single_measurement_with_led():
	enable_main_led()
	readings = take_single_measurement()
	disable_main_led()
	return readings

#Function to return the temperature in degrees C from the sensor
def get_temperature():
	temperature = read_reg(0x06)
	return temperature

#Function to return the temperature in degrees F from the sensor
def get_temperature_f():
	temperature = read_reg(0x06) * 1.8 + 32
	return temperature

#Function to turn on the main illumination LED
def enable_main_led():
	#Read the current state of the LEDs from the device
	current_state = read_reg(0x07)	
	#Set the bit for controlling the main LED to 1 (on) while
	#keeping the other bits as they were
	new_state = current_state | 0b00001000
	#Update the device
	write_reg(0x07, new_state)

#Function to turn off the main LED
def disable_main_led():
	#Read the current state of the LEDs from the device
	current_state = read_reg(0x07)
	#Set the bit controlling the main LED to 0 (off),
	# keep the other bits as they were
	new_state = current_state & 0b11110111
	#Update the device
	write_reg(0x07, new_state)

#Function to turn on the indicator LED
def enable_indicator_led():
	#Get the current state of the LEDs
	current_state = read_reg(0x07)
	#Set the bit controlling the indicator LED to 1 (on),
	# while keeping the other bits as they were
	new_state = curret_state | 0b00000001
	#Update the device
	write_reg(0x07, new_state)

#Function to turn off the indicator LED
def disable_indicator_led():
	#Get the current state of the LEDs
	current_state = read_reg(0x07)
	#Set the bit controlling the indicator LED to 0 (off),
	# while keeping the other bits as they were
	new_state = current_state & 0b11111110
	#Update the device
	write_reg(0x07, new_state)

#Function to set the measurement mode of the device, takes and int value of 0-3.
# 0 = continuous VBGY readings (rate dependent on integration time setting)
# 1 = continuous GYOR readings  (rate as above)
# 2 = continuous reading of all channels (rate as above)
# 3 = single measurement of all channels (no repeat readings/rate)
def set_measurement_mode(mode):
	#Check that the reqested mode is valid
	if mode in (0, 1, 2, 3):
		#Get the current settings
		current_state = read_reg(0x04)
		#Blank the current mode bits, keep the rest
		current_state = current_state & 0b11110011
		#The mode bits are no. 2&3, so shift the requested mode to match
		mode = mode << 2
		#Add the requested mode to the other current settings
		new_state = current_state | mode
		#Update the device
		write_reg(0x04, new_state)
	else:
		print("Error! set_measurement_mode requires a value of 0-3. Value given was " + str(mode) + ".")
	
#Function to set the current on the indicator LED, takes int value from 0-3
#0 = 1 mA, 1 = 2 mA, 2 = 4 mA, 3 = 8 mA
def set_indicator_current(current_level):
	#Check that the requested current_level is valid
	if current_level in (0, 1, 2, 3):
		#Get the current state of the LEDs
		current_state = read_reg(0x07)
		#Blank the current for the indicator LED
		new_state = current_state & 0b00111001
		#Indicator current bits are 1&2, so shift current_level to match
		current_level = current_level << 1
		#Insert the requested current_level into the LED control byte
		new_state = new_state | current_level
		#Update the device
		write_reg(0x07, new_state)
	else:
		print("Error! set_indicator_current requires a value of 0-3. Value given was " + str(current_level) + ".")
	
#Function to set the current on the LED, takes a value from 0-3
#0 = 12.5 mA, 1 = 25 mA, 2 = 50 mA, 3 = 100 mA
def set_led_current(current_level):
	#Check that the requested current_level is valid
	if current_level in (0, 1, 2, 3):
		#Get the current state of the LEDs
		current_state = read_reg(0x07)
		#Blank the bits controlling the bulb current
		new_state = current_state & 0b00001111
		#Bitshift the requested current_level to match the required position
		current_level = current_level << 4
		#Insert the current_level into the LED control byte
		new_state = new_state | current_level
		#Update the device with the new settings
		write_reg(0x07, new_state)
	else:
		print("Error! set_bulb_current requires a value of 0-3.  Value given was " + str(current_level) + ".")


#Function to soft reset the chip
def soft_reset():
	#Write the reset value to the register controlling the reset function
	write_reg(0x04, 0b10000000)
	#Wait for the device to reset (time determined experimentally,
	#the I2C bus seems to timeout with anything less?)
	time.sleep(0.8)

#Function to set the gain of the device.  Requires a value of 0-3
#0 = x1 gain, 1 = x3.7 gain, 2 = x16 gain, 3 = x64 gain
def set_gain(gain):
	#Check that the requested gain is valid
	if gain in (0,1,2,3):
		#Fetch the current setup register state
		current_state = read_reg(0x04)
		#Blank the bits controlling the gain, leave the rest as-is
		new_state = current_state & 0b11001111
		#The gain bits are no. 4 & 5, so shift gain to match
		gain = gain << 4
		#Add the new gain value to new_state
		new_state = new_state | gain
		#Write the new_state to the device
		write_reg(0x04, new_state)
	else:
		print("Error! set_gain requires a value of 0-3. Value given was " + str(gain) + ".")

#Function to set the integration time.  Takes a value between 1 and 255. This is
# multiplied by 2.8 ms to give the integration time. Modes 0 an 1 require one
#integration time to complete, modes 2 and 3 require two integration times.
def set_integration_time(time):
	#Check that the requested time is valid
	if (255 >= time >= 1):
		#Write the integration time to the INT_T register (0x05)
		write_reg(0x05, int(time))
	else:
		print("Error! set_integration_time requires a value of 1-255. Value given was " + str(time) + ".")

