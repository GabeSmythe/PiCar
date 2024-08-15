import yaml
from robot_hat import Servo
from robot_hat.utils import reset_mcu
from time import sleep


# Load configuration from config.yaml
with open('config.yaml', 'r') as file:
    config = yaml.safe_load(file)
    

motorIndexes = config['motorIndexes']
motorOffsets = config['motorOffsets']


reset_mcu()
sleep(0.2)

if __name__ == '__main__':
    for i in range(12):
        motorName = motorIndexes.get(i)
        if motorName is not None:
            zeroAngle = 0 + motorOffsets.get(motorName, 0)
            print(f"Servo {motorName} set to {zeroAngle}")
            Servo(i).angle(10)
            sleep(0.1)
            Servo(i).angle(zeroAngle)
            sleep(5)
    else:
        print(f"Servo index {i} is unused")
    while True:
        sleep(1)