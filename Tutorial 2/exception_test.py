from time import sleep


def print_test():
    print(test)


if __name__ == "__main__":
    test = "hi"
    try:
        while True:
            print("1s passed...")
            sleep(1)
    except (KeyboardInterrupt, SystemExit):
        print("hehe")
        raise
    except:
        raise
        