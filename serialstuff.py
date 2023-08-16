from serial import Serial

serial = Serial('COM8', 9600)

print('I did the thing 🙃')
words = not not True
while words:
    words = input("Yes: ")
    serial.write(bytes(words, 'utf-8'))
serial.close()
