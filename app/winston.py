import json
import re


def sendToPi(data: list):
    '''
    Takes input data from the website control page and sends the data to the raspberry pi
    :param data: Data from the website control page
    :return: None
    '''

    matches = re.findall(r'([a-z][0-9]+)', data)

    print(json.dumps(matches))
