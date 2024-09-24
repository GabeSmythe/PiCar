from picarx import Picarx
from robot_hat import Music, TTS
from robot_hat.utils import reset_mcu
from vilib import Vilib
import readchar
# import keyboard
import sys
import termios
import tty
import select
import threading
from time import sleep, time, strftime, localtime

import os
user = os.getlogin()
user_home = os.path.expanduser(f'~{user}')

OBJ_DISTANCE = 8
BACK_DISTANCE = 100
ROAD_EDGE_BACKUP = 40
FORWARD_SPEED = 5
FORWARD_TURN_DISTANCE = 40
RIGHT_ANGLE = 30
LEFT_ANGLE = -30
DRIVE_TIME = 0.5
GREYSCALE_OFFSET = 100
STOP_COLOUR = 'red'

reset_mcu()
sleep(0.2)

music = Music()
tts = TTS()

    
def readDistance():
    # print(f"Distance to next object = {px.ultrasonic.read()}")
    return px.ultrasonic.read()

def readGreyscale():
    # Read data
    greyscaleValues = px.get_grayscale_data()
    # Adjusting for tolerances
    greyscaleValues[0] += GREYSCALE_OFFSET
    greyscaleValues[2] += GREYSCALE_OFFSET
    greyscaleState = px.get_line_status(greyscaleValues) 
    return greyscaleState
    # print(f"Greyscale Status = {greyscaleState}")
    
def backUp(distance):
    px.set_dir_servo_angle(0)
    px.backward(distance)
    sleep(DRIVE_TIME)

def turnRight():
    px.set_dir_servo_angle(RIGHT_ANGLE)
    px.forward(FORWARD_TURN_DISTANCE)
    sleep(DRIVE_TIME)
    
def turnLeft():
    px.set_dir_servo_angle(LEFT_ANGLE)
    px.forward(FORWARD_TURN_DISTANCE)
    sleep(DRIVE_TIME)

def goForward():
    px.set_dir_servo_angle(0)
    px.forward(FORWARD_SPEED)
    # sleep(DRIVE_TIME/5)

# Function to run TTS in a separate thread
def speak(text):
    print(f"{text}")
    tts_thread = threading.Thread(target=tts.say, args=(text,))
    tts_thread.start()
    
# Play music in a separate thread
def play_music(music_file):
    music_thread = threading.Thread(target=music.music_play, args=(music_file,))
    music_thread.start()
    
# Function to check if a key has been pressed
def is_data():
    return select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], [])

if __name__ == '__main__':
    
    px = Picarx()
    
    # Settings for music and tts
    music.music_set_volume(20)
    tts.lang("en-US")

    # Create live video stream
    Vilib.camera_start(vflip=False,hflip=False)
    Vilib.display(local=True,web=True)
    
    # Wait for startup
    sleep(2) 
    
    print("Press q to quit program")
    
    # Set terminal to raw mode so we can capture keypresses without waiting for enter
    old_attr = termios.tcgetattr(sys.stdin)
    tty.setcbreak(sys.stdin.fileno())
    
    # Set courseFinished flag initially false, wait until finish line reached
    courseFinished = False
    completeOnce = False
    
    # Set stopFound to false initially and set colour to detect stop sign
    stopFound = False
    Vilib.color_detect(STOP_COLOUR)
    
    try:
        # Program Loop
        while True:
            # Non-blocking read of 1 char
            if is_data():
                key = sys.stdin.read(1)
                # Exit if q pressed
                if key.lower() =='q':
                    print("Q pressed, exiting loop")
                    break
                if key.lower() == 'r':
                    # Tell user
                    words = "Retrying course"
                    print(f"{words}")
                    speak(words)
                    courseFinished = False
        
            elif courseFinished == False:
                # Read front distance from ultrasonic
                distance = readDistance()
                # print(f"Distance = {distance}")
                # Read greyscale module data
                greyscaleState = readGreyscale()
                
                # If end of road reached, cease driving and await instructions
                if greyscaleState == [1,1,1]:
                    courseFinished = True
                    print("Course completed. Please press r to retry the course")
                    
                # Check if any stop sign is found   
                if Vilib.detect_obj_parameter['color_n']!=0 and 150 < Vilib.detect_obj_parameter['color_w'] < 400 and 100 < Vilib.detect_obj_parameter['color_h'] < 300 and stopFound == False:
                    # print(f"color_w = {Vilib.detect_obj_parameter['color_w']}, color_h = {Vilib.detect_obj_parameter['color_h']}")
                    px.stop() 
                    
                    # Tell user
                    words = "STOP SIGN DETECTED! Press c to continue"
                    speak(words)
                    
                    # Wait for c press
                    stopOverride = '0'
                    while (stopOverride.lower() != 'c'):
                        stopOverride = readchar.readkey()
                    stopFound = True
                    words = "Continuing course"
                    speak(words)
                        
                # If left side of road reached, back up and turn right
                if greyscaleState == [1,1,0] or greyscaleState == [1,0,0]:
                    
                    # Tell user
                    words = "Left side of road reached"
                    speak(words)
                    
                    # Back up and turn right
                    backUp(ROAD_EDGE_BACKUP)
                    turnRight()
                    
                # If right side of road reached, back up and turn left
                if greyscaleState == [0,1,1] or greyscaleState == [0,0,1]:
                    
                    # Tell user
                    words = "Right side of road reached"
                    speak(words)
                    
                    # Back up and turn left
                    backUp(ROAD_EDGE_BACKUP)
                    turnLeft()
                    
                # If object too close in front, back up and turn to the left
                if (0 < distance < OBJ_DISTANCE and courseFinished == False):
                    
                    # Tell user
                    words = "Obstacle Detected"
                    speak(words)
                    
                    # Back up and turn left
                    backUp(BACK_DISTANCE)
                    turnLeft()
                    
                    # If object still too close in front, back up and turn to the right
                    distance = readDistance()
                    if (0 < distance < OBJ_DISTANCE):
                        # Tell user
                        words = "Obstacle still detected!"
                        speak(words)
                        
                        # Back up and turn right twice
                        backUp(BACK_DISTANCE)
                        turnRight()
                        backUp(BACK_DISTANCE)
                        turnRight()                
                
                else:
                    # Drive forward
                    goForward()
            else:
                # If course has been completed
                px.stop() 
                
                if completeOnce == False:
                    # Declare our victory
                    words = "Course completed"
                    speak(words)
                    
                    # Play victory song :D
                    music.music_set_volume(50)
                    play_music('1-19. Water Park.mp3')
                    completeOnce = True
            
    finally:
        # Restore terminal settings
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_attr)
        print("Program exiting")
    
        # Shut down camera and exit program
        px.stop()
        Vilib.camera_close()
        sleep(0.1)
