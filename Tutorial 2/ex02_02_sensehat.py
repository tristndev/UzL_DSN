from sense_hat import SenseHat
from socket import gethostname

sense = SenseHat()

def clear_matrix():
	sense.clear()

def show_temp():
	temp = sense.get_temperature()
	sense.show_message("Temp: " + str(round(temp, 1)))

def show_pressure():
	pressure = sense.get_temperature()
	sense.show_message("Pressure: " + str(round(pressure, 1)))

def show_hostname():
	hostname = gethostname()
	sense.show_message("Hostname: " + hostname)

if __name__ == "__main__":
	print(">> Waiting for events...")
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