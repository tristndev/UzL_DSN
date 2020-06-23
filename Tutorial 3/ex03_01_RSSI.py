import serial
from sense_hat import SenseHat
from socket import gethostname
from xbee import XBee
from statistics import median

def clear_matrix():
    sense.clear()

def show_hostname():
    hostname = gethostname()
    sense.show_message("Hostname: " + hostname)

def receive_data(data):
    print("received data: ", data)
    if (data["rf_data"] == "ping"):
        # Received ping? -> Send pong back
        send_data("pong")
    elif (data["rf_data"] == "pong"):
        # Received pong? -> Store & calc RSSI
        rssi_list.append(ord(data["rssi]"]))
        print_current_rssi_median()
        
def send_data(data, dest_addr="\x00\x01"):
    xbee.send("tx",
              frame_id="\x00",
              dest_addr=dest_addr,
              data=data)

def init_rssi_calc(n_pings=10):
    dest_addr = "\x00\x01" # 2byte hex value (TODO: Set according to adress of destination XBee module)
    for i in range(n_pings):
        send_data("ping", dest_addr)

def print_current_rssi_median():
    med = median(rssi_list)
    print("Current RSSI median with {} received pongs: {}".format(len(rssi_list), med))
    

if __name__ == "__main__":
    sense = SenseHat()
    print(">> Opening serial port...")
    ser = serial.Serial("/dev/ttyUSB0", 9600)
    xbee = XBee(ser, callback=receive_data)

    rssi_list = []

    print(">> Waiting for events...")
    for event in sense.stick.get_events():
        if event.action == "pressed":
            if event.direction == "middle":
                print("** Event: Pressed.")
                clear_matrix()
            elif event.direction == "left":
                print("** Event: Left")
                init_rssi_calc()
            elif event.direction == "right":
                print("** Event: Right.")
                show_hostname()
