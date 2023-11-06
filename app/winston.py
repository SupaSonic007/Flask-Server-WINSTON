import json
import re
from serial import Serial

def sendToPi(data: list):
    '''
    Takes input data from the website control page and sends the data to the raspberry pi
    (Not implemented yet, and so it prints the serialised data instead)

    :param data: Data from the website control page
    :return: None
    '''

    # Fidn all matches where it's a letter and number e.g. f3 (Forward 3), r9 (Right 9), b2 (Back 2)
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
    