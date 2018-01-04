# AS7262-Pi

**Introduction**

This is a set of functions for using the Sparkfun AS7262 Visible Spectrometer (https://www.sparkfun.com/products/14347) with the Raspberry Pi.  The Default I2C address of the device is 0x49.  Requires the *SMBus*, *time* and *struct* Python modules, all installed on the Pi by default.

Please note that these were written for and have only been tested on the *visible* spectrometer board, not the similar AS7263 near infra-red board.

**Connecting the board**

The board has what Sparkfun calls Qwiic connectors, but it's possible to connect the board to the Raspberry Pi's GPIO pin headers with a little soldering.  Use jumper wires to connect GND to one of the Pi's GPIO Ground wires, 3v3 to the Pi's 3v3 pin, SDA to BCM2/GPIO3, and SCL to BCM3/GPIO5.  See pinout.xyz if you need help.  This script doesn't currently support interacting with the interrupt or reset pins.

**Suggested usage:**

1) Place this script in the same directory as your script, and import it

2) Use set_gain(gain) to set the gain (by default the Sparkfun Arduino library uses a gain value of 3, for x64 gain)

3) Use set_integration_time(time) to set the integration time (by default the Sparkfun Arduino library uses a value of 50, for 140ms cycle time)

4) Use set_measurement_mode(mode) to tell the board how often to take readings.  A value of 3 measures a single set of red, orange, yellow, green, blue and violet values.

5) Use get_calibrated_values() to return a list of 6 floats with values in the order ROYGBV.

# Functions:

* **read_reg(reg_to_read)**

Returns a single byte from a virtual register on the breakout.  reg_to_read should be the address of the register to read.


* **write_reg(reg_to_write_to, command_to_write)**

Function to write a single byte to a single virtual register on the breakout.  reg_to_write_to should be the address of the virtual register to be written to (BEFORE bit 7 is set to 1 to indicate a write, i.e. use the same address as for reading), command_to_write should be a single hex value to be written to that register.


* **take_single_measurement()**

Function to get the breakout to take a single set of ROYGBV readings and return them as a list of floats in the order ROYGBV.

* **take_single_measurement_with_led()**

The same as take_single_measurement(), but turns on the white LED on the breakout before measuring and disables it afterwards.


* **get_calibrated_values()**

Function to read, process and return stored calibrated ROYGBV values as a list of floats in the order ROYGBV.  Note that you MUST have used set_measurement_mode() to tell the device to take readings before you can fetch them with this function.


* **set_measurement_mode(mode)**

Tells the breakout how to take measurements, MUST be passed a value of 0, 1, 2 or 3.  Without setting this first no readings will be made and get_calibrated_values() will fail.

0 = continuous VBGY readings every (integration time * 2.8

1 = continuous GYOR readings every (integration time * 2.8) milliseconds

2 = continuous reading of all channels every (integration time * 2 * 2.8) milliseconds

3 = single measurement of all channels (no repeat readings/rate)


* **get_temperature()**

Returns the temperature in degrees C from the sensor


* **get_temperature_f()**

Returns the temperature in degrees F from the sensor


* **enable_main_led()**

Turns on the white LED on the breakout.  The brightness is controlled by set_led_current().


* **disable_main_led()**

Turns the white LED on the breakout off.


* **enable_indicator_led()**

Turns on the blue indicator LED on the breakout board.  The brightness is controlled by set_indicator_current()


* **disable_indicator_led()**

Turns the indicator LED off.


* **set_indicator_current(current_level)**

Sets the current provided to the indicator LED, MUST be passed a value of 0, 1, 2 or 3.  More current is brighter, the LED doesn't actually turn on until enable_indicator_led() is used.

0 = 1 mA 

1 = 2 mA

2 = 4 mA

3 = 8 mA
	

* **set_led_current(current_level)**

Sets the current provided to the white LED, MUST be passed a value of 0, 1, 2 or 3.  More current is brighter, the LED doesn't actually turn on until enable_main_led() is used.

0 = 12.5 mA 

1 = 25 mA

2 = 50 mA

3 = 100 mA


* **soft_reset()**

Soft resets the breakout with 0.8 second wait for the device to reset (this time was determined experimentally, anything much less seems to cause the I2C bus to timeout).


* **set_gain(gain)**

Sets the gain of the spectrometer.  More gain = higher readings, MUST be passed a value of 0, 1, 2 or 3.

0 = x1   gain

1 = x3.7 gain

2 = x16  gain

3 = x64  gain


* **set_integration_time(time)**

Sets the integration time of the readings.  Must be given an integer between 1 and 255, refer to the set_measurement_mode() section to see how this affects the time to take a reading.
