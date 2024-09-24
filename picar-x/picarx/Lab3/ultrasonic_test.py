from picarx import Picarx
import readchar

if __name__ == '__main__':
    px = Picarx()
    while True:
        key = readchar.readkey()
        if (key == "q" or key == "Q"):
            break
        elif (key == "d" or key == "D"):
            # distance = px.get_distance()
            # Using ultrasonic.read seems to be slightly more reliable
            distance = px.ultrasonic.read()
            print(distance)
    print("Program concluded")
