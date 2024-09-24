from picarx import Picarx
import readchar
px = Picarx()

print("Press q to exit, or anything else to get read")
while True:
    key = readchar.readkey()
    if key == ('q'):
        print("q pressed, program exiting")
        break
    else:
        # Read greyscale module data
        greyscaleValues = px.get_grayscale_data()
        # Adjusting for tolerance
        greyscaleValues[0] += 100
        greyscaleValues[2] += 100
        greyscaleState = px.get_line_status(greyscaleValues) 
        print(f"Adjusted Greyscale Status = {greyscaleState}")
        print(f"Adjusted Greyscale Values = {greyscaleValues}")