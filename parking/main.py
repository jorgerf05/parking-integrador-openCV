import sys
from detector import Detector
from selector import Selector

def main():

    for i in sys.argv:
        if i == "-s":
            selector = Selector()
            selector.start()

    dtr = Detector()
    dtr.start()

if __name__ == "__main__":main()