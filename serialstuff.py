# TEST FILE FOR SERIAL TO ARDUINO

from serial import Serial

serial = Serial('COM8', 9600)

words = True
while words:
    words = input("INPUT: ")
    serial.write(bytes(words, 'utf-8'))
serial.close()
