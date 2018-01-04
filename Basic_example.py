"""
An example of how to use the AS7262 functions to operate the board.  It begins
with some initial setup, and then puts the board into measurement mode 2, 
which continuously takes measurements for all colours.  This is returned as
a list called "results", which is then printed in a mostly human-readable form.
"""

#Import the script for the board
import AS7262_Pi as spec

#Reboot the spectrometer, just in case
spec.soft_reset()

#Set the gain of the device between 0 and 3.  Higher gain = higher readings
spec.set_gain(3)

#Set the integration time between 1 and 255.  Higher means longer readings
spec.set_integration_time(50)

#Set the board to continuously measure all colours
spec.set_measurement_mode(2)

#Run this part of the script until stopped with control-C
try:
	#Turn on the main LED
	spec.enable_main_led()
	#Do this until the script is stopped:
	while True:
		#Store the list of readings in the variable "results"
		results = spec.get_calibrated_values()
		#Print the results!
		print("Red    :" + str(results[0]))
		print("Orange :" + str(results[1]))
		print("Yellow :" + str(results[2]))
		print("Green  :" + str(results[3]))
		print("Blue   :" + str(results[4]))
		print("Violet :" + str(results[5]) + "\n")


#When the script is stopped with control-C
except KeyboardInterrupt:
	#Set the board to measure just once (it stops after that)
	spec.set_measurement_mode(3)
	#Turn off the main LED
	spec.disable_main_led()
	#Notify the user
	print("Manually stopped")	
