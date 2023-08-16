import json
import re
from serial import Serial

def sendToPi(data: list):
    '''
    Takes input data from the website control page and sends the data to the raspberry pi
    :param data: Data from the website control page
    :return: None
    '''

    matches = re.findall(r'([a-z][0-9]+)', data)

    print(json.dumps(matches))

def sendToArduino(data: int):
    '''
    Takes input data from the website control page and sends the data to the arduino
    :param data: Data from the website control page
    :return: None
    '''

    serial = Serial('COM8', 9600)

    serial.write(bytes(data, 'utf-8'))

    matches = re.findall(r'([a-z][0-9]+)', data)

    print(json.dumps(matches))