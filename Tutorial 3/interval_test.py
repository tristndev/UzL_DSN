import threading, sys

def interval_function():
    print("Interval function executed.")
    threading.Timer(4, interval_function).start()


if __name__=='__main__':
    interval_function()

    # Wait for input
    input("Press Enter to continue...")
    print("It goes on...")
    