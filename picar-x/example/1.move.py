import yaml
from picarx import Picarx
import time

# Load configuration from config.yaml
with open('config.yaml', 'r') as file:
    config = yaml.safe_load(file)
    

motorIndexes = config['motorIndexes']
motorOffsets = config['motorOffsets']


if __name__ == "__main__":
    try:
        # init picarx
        px = Picarx()

        # test motor
        px.forward(30)
        time.sleep(0.5)
        # test direction servo
        for angle in range(0, 35):
            px.set_dir_servo_angle(angle + motorOffsets["steer"])
            time.sleep(0.01)
        for angle in range(35, -35, -1):
            px.set_dir_servo_angle(angle + motorOffsets["steer"])
            time.sleep(0.01)
        for angle in range(-35, 0):
            px.set_dir_servo_angle(angle + motorOffsets["steer"])
            time.sleep(0.01)
        px.stop()
        time.sleep(1)
        # test cam servos
        for angle in range(0, 35):
            px.set_cam_pan_angle(angle + motorOffsets["pan"])
            time.sleep(0.01)
        for angle in range(35, -35, -1):
            px.set_cam_pan_angle(angle + motorOffsets["pan"])
            time.sleep(0.01)        
        for angle in range(-35, 0):
            px.set_cam_pan_angle(angle + motorOffsets["pan"])
            time.sleep(0.01)
        for angle in range(0, 35):
            px.set_cam_tilt_angle(angle + motorOffsets["pan"])
            time.sleep(0.01)
        for angle in range(35, -35,-1):
            px.set_cam_tilt_angle(angle + motorOffsets["pan"])
            time.sleep(0.01)        
        for angle in range(-35, 0):
            px.set_cam_tilt_angle(angle + motorOffsets["pan"])
            time.sleep(0.01)
    finally:
        px.stop()
        time.sleep(0.2)


