"""A Demo script to take measurements from the SparkFun AS7262 Visible Spectral Sensor Breakout and display it on a 
Pimoroni Unicorn HAT HD in a bar-graph like format.  Requires the spectrometer.py file to be in the same directory."""

import unicornhathd
import time
import spectrometer as spectro

"""Set up the spectrometer: reset it, set gain and integration time as per Sparkfun's default values in their Arduino script,
turn off the indicator LED (for some reason it sometimes comes on after resetting the spectrometer)."""
spectro.soft_reset()
spectro.set_gain(3)
spectro.set_integration_time(50)
spectro.disable_indicator_led()

#Set the brightness of the Unicorn HAT HD from 0.0 - 0.9, default 0.5
unicornhathd.brightness(0.5)

#Set the rotation of the Unicorn HAT HD in 90-degree increments
unicornhathd.rotation(0)

"""Create a dictionary called colours{}: each colour has an X value for the colour's starting column on the Unicorn HAT HD, 
the X coordinate of the corresponding HAT column end, and a red, green and blue value in that order. """
colours = {"Red":[2,4,255,0,0], "Orange":[4,6,255,128,0], "Yellow":[6,8,192,192,0],
	"Green":[8,10,0,255,0], "Blue":[10,12,0,0,255], "Violet":[12,14,128,0,255]}

#Take a colour reading and display it as a bar on the Unicorn HAT HD
def updateColour(colour, value):
  #Print the colour name and value associated with it
	#print(str(colour) + " : " + str(value))
  #Get the X coordinate of the first bar for the colour
	xCoord1 = colours[colour][0]
  #Get the X coordinate of the second bar for the colour
	xCoord2 = colours[colour][1]
  #Get the R, G and B values for the colour
	r = colours[colour][2]
	g = colours[colour][3]
	b = colours[colour][4]
  
	#If the magnitude of a colour is >0, set that many pixels to that colour
  #Stop extreme values overrunning the size of the HAT
	if value > 16:
		value = 16
  #Set the two coloumns of the bar for the colour:
  for x in range(xCoord1, xCoord2):
    #Set the height of the bars
		for y in range (0,value):
			unicornhathd.set_pixel(x,y,r,g,b)
	#Blank unused pixels in those columns
	for x in range (xCoord1, xCoord2):
		for y in range (value, 16):
			unicornhathd.set_pixel(x,y,0,0,0)



#Set to continuous ROYGBV measurements
spectro.set_measurement_mode(2)
#Enable the main LED
spectro.enable_main_led()
#Set the gain to x64
spectro.set_gain(3)
#Set the integration time to ~150 ms
spectro.set_integration_time(50)

try:
	while True:

    #Get the ROYGBV readings
		results = spectro.get_calibrated_values()

    #For each colour in results[], update the corresponding bar on the Unicorn HAT HD
		updateColour("Red", int(results[0]/3200))
		updateColour("Orange", int(results[1]/3200))
		updateColour("Yellow", int(results[2]/3200))
		updateColour("Green", int(results[3]/3200))
		updateColour("Blue", int(results[4]/3200))
		updateColour("Violet", int(results[5]/3200))

		#Display the new values on the Unicorn HAT HD
		unicornhathd.show()

#Clean Shutdown when stopped with Ctrl-C
except KeyboardInterrupt:
	unicornhathd.clear()
	unicornhathd.show()
	spectro.disable_main_led()
	spectro.set_measurement_mode(3)
	print("	Manually stopped.")

