import cv2
import socket
import struct
import sys

from drawer import Drawer
from model import Model

HOST = ''
PORT = 8080

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

try:
    s.bind((HOST, PORT))
except socket.error as e:
    print('Bind failed. Error: ' + str(e))
    sys.exit()

s.listen(10)

conn, addr = s.accept()

print('Connected by: ' + str(addr))

buf = ''

while len(buf) < 4:
    buf += conn.recv(4 - len(buf))

size = struct.unpack('!i', buf)

with open('test.png', 'wb') as img:
    while True:
        data = conn.recv(1024)

        if not data:
            break

        img.write(data)

img.close()
conn.close()

draw = Drawer()
draw.img = cv2.imread(filename='test.png')
char_images = draw.get_contours()

for cimg in char_images:
    Model().predict(img=Drawer.convert_to_emnist(img=cimg))

s.close()
