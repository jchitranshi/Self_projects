import socket

HOST='127.0.0.1'
PORT=12345
with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as my_socket:
	my_socket.connect((HOST,PORT))
	my_socket.sendall(b'Hello World from socket!!')
	data=my_socket.recv(1024)
print("Received",repr(data))