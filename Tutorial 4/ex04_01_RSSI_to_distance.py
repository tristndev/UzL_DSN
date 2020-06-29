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
    if (data["rf_data"] == b"ping"):
        # Received ping? -> Send pong back
        send_data("pong")
    elif (data["rf_data"] == b"pong"):
        # Received pong? -> Store & calc RSSI
        rssi_list.append(ord(data["rssi"]))
        print_current_rssi_median()

        if data["source_addr"] not in rssi_list:
            rssi_dict[data["source_addr"]] = []
        rssi_dict[data["source_addr"]].append(ord(data["rssi"]))
        
def send_data(data, dest_addr="\x00\x0A"):
    xbee.send("tx",
              frame_id="\x00",
              dest_addr=dest_addr,
              data=data)

def init_rssi_calc(n_pings=10):
    rssi_list = []
    dest_addr = "\x00\x0A" # 2byte hex value (TODO: Set according to adress of destination XBee module)
    for i in range(n_pings):
        send_data("ping", dest_addr)

def print_current_rssi_median():
    med = median(rssi_list)
    print("Current RSSI median with {} received pongs: {}".format(len(rssi_list), med))
    dist = dist_from_rssi(med)
    print("Current dist from RSSI: dist = {}".format(dist))

def dist_from_rssi(rssi):
    n = 2.8 # path loss variable from 2 to 4
    A = 33 # TODO: Measure reference RSSI (1m distance)
    # RSSI = -10 * n * log_10(d) + A
    # => Transformed to
    # d = 10^(A/10n)
    dist = 10**(A/10*n)
    return dist

def three_anchor_bbox():
    dist_dict = {}
    for anchor in rssi_dict:
        dist_dict[anchor] = dist_from_rssi(median(rssi_dict[anchor]))

    x = 1/2 * (min([anchor_positions[anchor][0] + dist_dict[anchor] for anchor in anchor_positions]) + \
        max([anchor_positions[anchor][0] - dist_dict[anchor] for anchor in anchor_positions]))
    
    y = 1/2 * (min([anchor_positions[anchor][1] + dist_dict[anchor] for anchor in anchor_positions]) + \
        max([anchor_positions[anchor][1] - dist_dict[anchor] for anchor in anchor_positions]))

    print(">> BBox calculation done: X: {} | Y: {}".format(x,y))

def three_anchor_multilat():
    print("... Starting multilateration.")
    dist_dict = {}
    for anchor in rssi_dict:
        dist_dict[anchor] = dist_from_rssi(median(rssi_dict[anchor]))

    # https://github.com/kamalshadi/Localization
    import localization as lx
    P=lx.Project(mode='2D',solver='LSE')
    
    print("... adding anchors")
    for anchor in anchor_positions:
        P.add_anchor(anchor, anchor_positions[anchor])

    t,label = P.add_target()

    print("... adding measurements")
    for dist in dist_dict:
        P.add_measure(dist, dist_dict[dist])
    
    print("... calculating...")
    P.solve()

    print("> Done! Multilat result:", t.loc)
    

def broadcast_ping():
    rssi_dict = {}
    # Broadcast ping
    send_data("ping", "\xFF\xFF")

if __name__ == "__main__":
    sense = SenseHat()
    print(">> Opening serial port...")
    ser = serial.Serial("/dev/ttyUSB1", 9600)
    xbee = XBee(ser, callback=receive_data)

    rssi_list = []
    rssi_dict = {}
    
    ## TODO: Fill anchor position dictionary!
    anchor_positions = {
        "add1": (0, 1),
        "add2": (0, 3),
        "add3": (0, 4)
    }

    print(">> Waiting for events...")
    print("Middle: clear_matrix, left: init_rssi_calc, right: three_anchor_bbox, down: broadcast_ping")
    print("Sequence: broadcast_ping -> three_anchor_bbox / three_anchor_multilat")
    while True:
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
                    three_anchor_bbox()
                elif event.direction == "down":
                    print("** Event: Down")
                    broadcast_ping()
                elif event.direction == "up":
                    print("** Event: up")
                    three_anchor_multilat()
