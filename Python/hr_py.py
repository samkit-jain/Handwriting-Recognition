import os
import socket
import sys
import struct
from android_rec import ret_val


HOST = ''
PORT = 8080

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

try:
	s.bind((HOST, PORT))
except socket.error, msg:
	print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
	
	sys.exit()

s.listen(10)

conn, addr = s.accept()

print "Connected by: ", addr

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

print ret_val()

s.close()