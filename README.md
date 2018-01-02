# SparkFun-AS7262-Pi-
Python script for using the Sparkfun AS7262 Visible Spectrometer with the Raspberry Pi.  The Default I2C address of the device is 0x49.

Requires the SMBus, time and struct Python modules (all installed on the Pi by default).

# Functions:

def read_reg(reg_to_read):
Returns a single byte from a virtual register on the breakout.  reg_to_read should be the address of the register to read.


def write_reg(reg_to_write_to, command_to_write):
Function to write a single byte to a single virtual register on the breakout.  reg_to_write_to should be the address of the virtual register to be written to (BEFORE bit 7 is set to 1 to indicate a write, i.e. use the same address as for reading), command_to_write should be a single hex value to be written to that register.


def take_single_measurement():
Function to get the breakout to take a single set of ROYGBV readings and return them as a list of floats in the order ROYGBV.


def get_calibrated_values():
Function to read, process and return stored calibrated ROYGBV values as a list of floats in the order ROYGBV.  Note that you MUST have used set_measurement_mode() to tell the device to take readings before you can fetch them with this function.



def take_single_measurement_with_led():
The same as take_single_measurement(), but turns on the white LED on the breakout before measuring and disables it afterwards.

def get_temperature():
Returns the temperature in degrees C from the sensor


def get_temperature_f():
#Returns the temperature in degrees F from the sensor


def enable_main_led():
Turns on the white LED on the breakout.  The brightness is controlled by set_led_current().


def disable_main_led():
Turns the white LED on the breakout off.


def enable_indicator_led():
Turns on the blue indicator LED on the breakout board.  The brightness is controlled by set_indicator_current()


def disable_indicator_led():
Turns the indicator LED off.


def set_measurement_mode(mode):
Tells the breaout how to take measurements, MUST be passed a value of 0, 1, 2 or 3.  Without setting this first no readings will be made and get_calibrated_values() will fail.
0 = continuous VBGY readings every (integration time * 2.8 ms)
1 = continuous GYOR readings every (integration time * 2.8 ms)
2 = continuous reading of all channels every (integration time * 2 * 2.8 ms)
3 = single measurement of all channels (no repeat readings/rate)


def set_indicator_current(current_level):
Sets the current provided to the indicator LED, MUST be passed a value of 0, 1, 2 or 3.  More current is brighter, the LED doesn't actually turn on until enable_indicator_led() is used.
0 = 1 mA 
1 = 2 mA
2 = 4 mA
3 = 8 mA
	

def set_led_current(current_level):
Sets the current provided to the white LED, MUST be passed a value of 0, 1, 2 or 3.  More current is brighter, the LED doesn't actually turn on until enable_main_led() is used.
0 = 12.5 mA 
1 = 25 mA
2 = 50 mA
3 = 100 mA


def soft_reset():
Soft resets the breakout with 0.8 second wait for the device to reset (this time was determined experimentally, anything much less seems to cause the I2C bus to timeout).


Function to set the gain of the device.  Requires a value of 0-3
def set_gain(gain):
Sets the gain of the spectrometer.  More gain = higher readings, MUST be passed a value of 0, 1, 2 or 3.
0 = x1   gain
1 = x3.7 gain
2 = x16  gain
3 = x64  gain


def set_integration_time(time):
Sets the integration time of the readings.  Must be given an integer between 1 and 255, refer to the set_measurement_mode() section to see how this affects the time to take a reading.
