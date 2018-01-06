
# AS7262-Pi: 6 colour spectroscopy for the Raspberry Pi!

![Rainbows](rainbows.gif)

**Introduction**

This is a set of functions for using the [Sparkfun AS7262 Visible Spectrometer Breakout](https://www.sparkfun.com/products/14347) with the Raspberry Pi.  Please note that these were written for and have only been tested on the *visible* spectrometer board, not the similar AS7263 near infra-red board.

There are 5 files in this repo: 
1) README.md is the file you're currently reading and contains information about how to use this repo.
2) AS7262_Pi.py contains all of the functions which make the AS7262 board work with the Pi.
3) Basic_example.py is, well, a basic example of how to use the AS7262 board with the Pi.
4) UHHD_spectrometer.py is a more advanced demo script which displays the readings of the AS7262 on a Pimoroni Unicorn HAT HD in a bar chart-like format.  You can see it in action in the .gif at the top of this page.
5) Rainbows.gif is is the .gif at the top of the page, made using the UHHD_spectrometer.py script.

The AS7262 communicates with the Pi using the I2C bus.  The I2C address of the device is 0x49, and the script requires the *SMBus*, *time* and *struct* Python modules, all installed on the Pi by default.

**Connecting the board**

The board has what Sparkfun calls Qwiic connectors, but it's possible to connect the board to the Raspberry Pi's GPIO pin headers with a little soldering.  Use jumper wires to connect the breakout's GND to one of the Pi's GPIO Ground wires, 3v3 to the Pi's 3v3 pin, SDA to BCM2/GPIO3, and SCL to BCM3/GPIO5.  See [Pinout.xyz](https://www.pinout.xyz) if you need help.  This script doesn't currently support interacting with the interrupt or reset pins.

**Suggested usage:**

0) Ensure that I2C is enabled on your Pi: run `sudo raspi-config` in a terminal, and then go to `Interfacing Options` > `I2C` > `yes`.

1) Download this repo by running `git clone https://github.com/Shoe-Pi/AS7262_Pi` in a terminal.

2) Place the file called "AS7262_Pi.py" in the same directory as your script, and import it.

3) Use `set_gain(gain)` to set the gain (by default the Sparkfun Arduino library for the AS7262 uses a gain value of 3, for x64 gain).

4) Use `set_integration_time(time)` to set the integration time (by default the Sparkfun Arduino library uses a value of 50, for 140ms cycle time).

5) Use `set_measurement_mode(mode)` to tell the board how often to take readings.  A value of 3 measures a single set of red, orange, yellow, green, blue and violet values.

6) Use `get_calibrated_values()` to return a list of 6 floats with values in the order ROYGBV.

# Functions:


* **take_single_measurement()**

Function to get the breakout to take a single set of red, orange, yellow, green, blue and violet readings and return them as a list of 6 floats in the order ROYGBV.


* **take_single_measurement_with_led()**

The same as `take_single_measurement()`, but turns on the white LED on the breakout before measuring and disables it afterwards.


* **get_calibrated_values()**

Function to read, process and return stored calibrated red, orange, yellow, green, blue and violet values as a list of floats in the order ROYGBV.  Note that once `get_calibrated_readings()` is used a flag is set on the AS7262 stating that no new values are available to be read until the device takes another set of readings.  For `set_measurement_mode()` values of 0-2 this shouldn't cause issues because the board will continuously take new readings.  However, in measurement mode 3 (single measurement mode) subsequent attempts to retrieve readings will fail until the board is put back into mode 3 to take another set of readings.  


* **set_measurement_mode(mode)**

Tells the breakout how to take measurements, MUST be passed a value of 0, 1, 2 or 3.  Without setting this first no readings will be made and `get_calibrated_values()` will fail.  Defaults to mode 2.

0 = continuous violet, blue, green and yellow readings every (integration time * 2.8) milliseconds.

1 = continuous green, yellow, orange and red readings every (integration time * 2.8) milliseconds.

2 = continuous readings of all channels (violet, blue, green, yellow, orange and red) every (integration time * 2 * 2.8) milliseconds.

3 = single measurement of all channels (no repeat readings/rate).


* **enable_main_led()**

Turns on the breakout's white LED.  The brightness is controlled by `set_led_current()`.  The LED is off by default.


* **disable_main_led()**

Turns the breakout's white LED off.


* **set_led_current(current_level)**

Sets the current provided to the white LED, MUST be passed a value of 0, 1, 2 or 3.  More current is brighter, note that the LED doesn't actually turn on until `enable_main_led()` is used.  Defaults to 12.5 mA (mode 0).

0 = 12.5 mA 

1 = 25 mA

2 = 50 mA

3 = 100 mA


* **enable_indicator_led()**

Turns on the breakout's blue indicator LED.  The brightness is controlled by `set_indicator_current()`.  The LED is off by default.


* **disable_indicator_led()**

Turns the breakout's indicator LED off.


* **set_indicator_current(current_level)**

Sets the current provided to the indicator LED, MUST be passed a value of 0, 1, 2 or 3.  More current is brighter, note that the LED doesn't actually turn on until `enable_indicator_led()` is used.  Defaults to 1 mA (mode 0).

0 = 1 mA 

1 = 2 mA

2 = 4 mA

3 = 8 mA
	

* **soft_reset()**

Soft resets the breakout with a 0.8 second wait for the device to reset (this time was determined experimentally, anything less seems to cause the I2C bus to timeout).  This should reset all control registers to their default values.


* **set_gain(gain)**

Sets the gain of the spectrometer.  More gain = higher readings, MUST be passed an integer value of 0, 1, 2 or 3.  Defaults to x1 (mode 0).

0 = x1   gain

1 = x3.7 gain

2 = x16  gain

3 = x64  gain


* **set_integration_time(time)**

Sets the integration time of the readings.  Higher values mean longer measurements but are less prone to noise (?).  Must be given an integer between 1 and 255, refer to the `set_measurement_mode()` section to see how this affects the time to take a reading.  Defaults to 255.


* **get_temperature()**

Returns the temperature in °C from the sensor using the built in temperature sensor.  This only seems to return integers.


* **get_temperature_f()**

Returns the temperature in °F from the sensor by converting the centrigade value of `get_temperature()` to °F.


* **read_reg(reg_to_read)**

Returns a single byte from a virtual register on the breakout.  `reg_to_read` should be the address of the register to read.  The AS7262 uses an odd virtual register system which makes it more complicated to read data from the device than usual.  If that makes no sense then don't worry, this function is just here so that the other functions can use it: you won't need to use it yourself.


* **write_reg(reg_to_write_to, command_to_write)**

Function to write a single byte to a single virtual register on the breakout.  `reg_to_write_to` should be the address of the virtual register to be written to (BEFORE bit 7 is set to 1 to indicate a write, i.e. use the same address as for reading), `command_to_write` should be a single hex value to be written to that register.  Like I2C reads, the AS7262 uses a slightly odd system for writing to registers and so this function handles that.
