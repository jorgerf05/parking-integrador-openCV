import sys
from detector import Detector
from selector import Selector

def main():

    for arg in sys.argv:
        if arg == "-s" or arg == "--setup":
            selector = Selector()
            selector.start()
            sys.exit()

    dtr = Detector()
    dtr.start()

if __name__ == "__main__":main()
