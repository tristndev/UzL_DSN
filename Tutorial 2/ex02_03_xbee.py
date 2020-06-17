import serial 
from sense_hat import SenseHat
from socket import gethostname

def clear_matrix():
	sense.clear()

def show_temp():
	temp = sense.get_temperature()
	msg = "Temp: " + str(round(temp, 1))
	sense.show_message(msg)
	ser.write(msg)

def show_pressure():
	pressure = sense.get_temperature()
	msg = "Pressure: " + str(round(pressure, 1))
	sense.show_message(msg)
	ser.write(msg)
	
def show_hostname():
	hostname = gethostname()
	msg = "Hostname: " + hostname
	sense.show_message(msg)
	ser.write(msg)

if __name__ == "__main__":
	try: 
		sense = SenseHat()
		ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=.5) # open serial port
		print(">> Waiting for events...")
		while True:
			# Check Sense Hat
			for event in sense.stick.get_events():
				if event.action == "pressed":
					print("** Event: Pressed.")
					clear_matrix()
				elif event.action == "up":
					print("** Event: Up.")
					show_temp()
				elif event.action == "left":
					print("** Event: Left")
					show_pressure()
				elif event.action == "right":
					print("** Event: Right.")
					show_hostname()
			
			# Check serial bus
			x = ser.readline()
			print("serial input: " + str(x))
	except (KeyboardInterrupt, SystemExit):
		ser.close()
		raise
	except:
		raise