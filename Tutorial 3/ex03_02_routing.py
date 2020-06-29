import serial
from sense_hat import SenseHat
from socket import gethostname
from xbee import XBee
from statistics import median
import threading

def clear_matrix():
    sense.clear()

def show_hostname():
    hostname = gethostname()
    sense.show_message("Hostname: " + hostname)

def receive_data(data):
    print("received data: ", data)
    if (data["rf_data"] == b"ping"):
        # Received ping? -> Send pong back
        send_data("pong")
    elif (data["rf_data"] == b"pong"):
        # Received pong? -> Store RSSI
        rssi_dict[data["source_addr"]] = {"rssi": data["rssi]"],
                                          "last_ping_counter": ping_counter}
        # Remove dead nodes
        cleanse_rssi_dict()
    elif data["rf_data"] == b"msg1":
        # I am node B
        node_b_wrapper(data)
    elif data["rf_data"] == b"msg2":
        i_am_node("C")

def cleanse_rssi_dict(remove_after_rounds = 3):
    """
    Goes through the `rssi_dict` and removes all entries where the ping counter is
    smaller than the current round (`ping_counter`) minus `remove_after_rounds`
    """
    for key in rssi_dict:
        if rssi_dict[key]["last_ping_counter"] < ping_counter - remove_after_rounds:
            del rssi_dict[key]

        
def send_data(data, dest_addr="\x00\x01"):
    """
    Sends given data to a given destination address.
    """
    print("## send_data(): data: {}, destination: {}".format(data, dest_addr))
    xbee.send("tx",
              frame_id="\x00",
              dest_addr=dest_addr, # 2byte hex value (TODO: Set according to adress of destination XBee module)
              data=data)

def ping_routine(interval=10):
    """
    Scheduled ping routine (every `interval` seconds)
    """
    ping_counter += 1
    send_data("ping", dest_addr="\xFFXFF") # broadcast ping
    threading.Timer(interval, ping_routine).start()

def start_distribution():
    """
    Starts distribution of the message according to exercise 2c)
    """
    b_addr = get_best_connection()
    
    send_data("msg1", dest_addr=b_addr)
    i_am_node("A")

def get_best_connection():
    """
    Returns the address with smallest rssi from rssi_dict.
    """
    return min(rssi_dict.keys(), key= (lambda x: rssi_dict[x]["rssi"]))

def node_b_wrapper(data):
    """
    Wrapper function for everything Node B has to do.
    """
    node_a_addr = data["source_addr"]
    my_addr = "" # TODO: What is my address?
    node_b_c_addr_list = [x for x in rssi_dict.keys() if x not in [node_a_addr, my_addr]]
    for addr in node_b_c_addr_list:
        send_data("msg2", addr)

def i_am_node(node):
    if node == "A":
        show_number(0, 255, 0, 0)
        print("!!! I am node A")
    if node == "B":
        show_number(1, 0, 255, 0)
        print("!!! I am node B")
    if node in ["C", "D"]:
        show_number(2, 0, 0, 255) 
        print("!!! I am node C / D")


if __name__ == "__main__":
    sense = SenseHat()
    print(">> Opening serial port...")
    ser = serial.Serial("/dev/ttyUSB0", 9600)
    xbee = XBee(ser, callback=receive_data)
    
    rssi_dict = {}
    ping_counter = 0
    ping_routine(interval=10)

    print(">> Waiting for events...")
    print("   Press <middle> to start distribution of messages.")
    print("   Press <up> to clear the matrix.")
    while True:
        for event in sense.stick.get_events():
            if event.action == "pressed":
                if event.direction == "middle":
                    print("** Event: Pressed.")
                    start_distribution()
                elif event.direction == "right":
                    print("** Event: Right.")
                    show_hostname()
                elif event.direction == "up":
                    print("** Event: Up")
                    clear_matrix()




## ========================
#  ---- UTIL FUNCTIONS ----
## ========================

OFFSET_LEFT = 1
OFFSET_TOP = 2

NUMS = [1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1,  # 0
        0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0,  # 1
        1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 1, 1,  # 2
        1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1,  # 3
        1, 0, 0, 1, 0, 1, 1, 1, 1, 0, 0, 1, 0, 0, 1,  # 4
        1, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 1,  # 5
        1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1,  # 6
        1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 0,  # 7
        1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1,  # 8
        1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 1, 0, 0, 1]  # 9

def show_digit(val, xd, yd, r, g, b):
    offset = val * 15
    for p in range(offset, offset + 15):
        xt = p % 3
        yt = (p-offset) // 3
        sense.set_pixel(xt+xd, yt+yd, r*NUMS[p], g*NUMS[p], b*NUMS[p])


def show_number(val, r, g, b):
    """
    val: up to 2 digit value to be displayed
    r,g,b: 0...255 integer for colors
    """
    abs_val = abs(val)
    tens = abs_val // 10
    units = abs_val % 10
    if (abs_val > 9):
        show_digit(tens, OFFSET_LEFT, OFFSET_TOP, r, g, b)
    show_digit(units, OFFSET_LEFT+4, OFFSET_TOP, r, g, b)