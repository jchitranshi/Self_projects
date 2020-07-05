import socket

HOST='127.0.0.1'
PORT=12345
#AF_IET addr family for ip4 and SOC_STREAM for tcp connection
with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as my_socket:
	my_socket.bind((HOST,PORT))
	my_socket.listen()
	conn,addr=my_socket.accept()
	with conn:
		print("Connected by",addr)
		while True:
			data=conn.recv(1024)
			if not data:
				break
			conn.sendall(data)
