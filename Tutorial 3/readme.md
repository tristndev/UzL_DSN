# README

## Ex. 01: RSSI

### TODO RSSI

* [ ] Find out and set (see `# TODO` comment) destination address.

## Ex. 02: Routing

### Short Summaries

#### Ping / Discovery behavior

* Every 10s, the nodes broadcast a ping to all other nodes who reply with a `pong`.
* When a `pong` is received, the node stores the RSSIs for the sender node in a dictionary, along with a `ping_counter`. 
* If a node sends no new `pong` after 3 rounds, it is removed from the `rssi_dict`.

#### Routing

1. One Node starts as Node A (according to Exercise 2), when the joystick is pressed. It displays a 0 and sends `msg1` to node B with the minimum RSSI according to `rssi_dict`.
2. Node B receives `msg1` and displays a 1 on the LED matrix. It then sends `msg3` to both remaining nodes.
3. Nodes C and D receive `msg2` and display a 2 on the matrix.

### TODO Routing

* [ ] Find out and set own address (if needed)? (see `# TODO` comment)