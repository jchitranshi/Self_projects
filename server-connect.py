#https://levelup.gitconnected.com/program-your-first-multiple-user-network-game-in-python-9f4cc3650de2
import tkinter as tk
import socket
import threading
#import thread
from _thread import *
from time import sleep

window = tk.Tk()
window.title("Sever")

# Top frame consisting of two buttons widgets (i.e. btnStart, btnStop)
topFrame = tk.Frame(window)
btnStart = tk.Button(topFrame, text="Start", command=lambda : start_server())
btnStart.pack(side=tk.LEFT)
btnStop = tk.Button(topFrame, text="Stop", command=lambda : stop_server(), state=tk.DISABLED)
btnStop.pack(side=tk.LEFT)
topFrame.pack(side=tk.TOP, pady=(5, 0))

# Middle frame consisting of two labels for displaying the host and port info
middleFrame = tk.Frame(window)
lblHost = tk.Label(middleFrame, text = "Address: X.X.X.X")
lblHost.pack(side=tk.LEFT)
lblPort = tk.Label(middleFrame, text = "Port:XXXX")
lblPort.pack(side=tk.LEFT)
middleFrame.pack(side=tk.TOP, pady=(5, 0))

# The client frame shows the client area
clientFrame = tk.Frame(window)
lblLine = tk.Label(clientFrame, text="**********Client List**********").pack()
scrollBar = tk.Scrollbar(clientFrame)
scrollBar.pack(side=tk.RIGHT, fill=tk.Y)
tkDisplay = tk.Text(clientFrame, height=10, width=30)
tkDisplay.pack(side=tk.LEFT, fill=tk.Y, padx=(5, 0))
scrollBar.config(command=tkDisplay.yview)
tkDisplay.config(yscrollcommand=scrollBar.set, background="#F4F6F7", highlightbackground="grey", state="disabled")
clientFrame.pack(side=tk.BOTTOM, pady=(5, 10))


server = None
HOST = "127.0.0.1"#0.0.0.0"
PORT = 23456#8080
client_name = " "
clients = []
clients_names = []
player_data = []
lock =threading.Lock()


# Start server function
def start_server():
    global server, HOST, PORT # code is fine without this
    btnStart.config(state=tk.DISABLED)
    btnStop.config(state=tk.NORMAL)

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print(socket.AF_INET)
    print(socket.SOCK_STREAM)
    #server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen(5)  # server is listening for client connection
    #print("start_server after listen")

    threading._start_new_thread(accept_clients, (server, " "))
    #threading.Thread(target=accept_clients,args=(server," "))

    #print("start_server after statrting new thread")

    lblHost["text"] = "Address: " + HOST
    lblPort["text"] = "Port: " + str(PORT)


# Stop server function
def stop_server():
    global server
    btnStart.config(state=tk.NORMAL)
    btnStop.config(state=tk.DISABLED)

def send_receive_client_message(client_connection,client_ip_addr):
	global server,client_name,clients,player_data,player0,player1
	#connect with server and send client data to server
	client_msg=""
	
	#send welcome msg to client
	client_name= client_connection.recv(1024)
	client_name= client_name.decode('ASCII')
	#print("send_receive_client_msg after recv name:",client_name)
	if len(clients)<2:
		client_connection.send(b"welcome1")
	else:
		client_connection.send(b"welcome2")
	#print("send recv client after send ",client_name)

	clients_names.append(client_name)
	update_client_names_display(clients_names)#update clients name display

	if len(clients) > 1:
		sleep(1)
		#send opponent name
		temp="opponent_name$"+clients_names[1]
		d = temp.encode("ASCII")
		clients[0].send(d)
		temp="opponent_name$"+clients_names[0]
		d= temp.encode("ASCII")
		clients[1].send(d)
	#go to sleep

	while True:
		data1=client_connection.recv(1024)
		data = data1.decode('ASCII')
		#print("data---------------\n",data)
		if not data:
			break

		#get player choice from received data
		player_choice=data[12:len(data)]
		#print("~~~~~~~~~~~~~~~~~~~~~",player_choice)

		msg={
			"choice":player_choice,
			"socket":client_connection
		}
		#print("*******************",len(player_data))

		if len(player_data)<2:
			player_data.append(msg)

		if len(player_data)==2:
			#send player 1 choice to player 2 and vice versa
			temp = "$opponent_choice"+player_data[1].get("choice")
			#print("&&&&&&&&&&&&&",temp)
			d = temp.encode('ASCII')
			player_data[0].get("socket").send(d)
			temp ="$opponent_choice"+player_data[0].get("choice")
			#print("&&&&&&&&&&&&&",temp)
			d =temp.encode('ASCII')
			player_data[1].get("socket").send(d)
			player_data = []
	# find the client index then remove from both lists(client name list and connection list)
	idx = get_client_index(clients, client_connection)
	del clients_names[idx]
	del clients[idx]
	client_connection.close()
	update_client_names_display(clients_names)  # update client names display


def accept_clients(the_server,y):
	while True:
		if len(clients)<2:
			client,addr=the_server.accept()
			#with lock:
			#	print("Connected by:",addr)
				#print("latest name : ",repr(client.recv(1024)))
			clients.append(client)

			#use a thread so as not to clog a UI thread
			#threading.Thread(target=send_receive_client_message,args=(client,addr))
			threading._start_new_thread(send_receive_client_message,(client,addr))



# Return the index of the current client in the list of clients
def get_client_index(client_list, curr_client):
    idx = 0
    for conn in client_list:
        if conn == curr_client:
            break
        idx = idx + 1

    return idx


# Update client name display when a new client connects OR
# When a connected client disconnects
def update_client_names_display(name_list):
    tkDisplay.config(state=tk.NORMAL)
    tkDisplay.delete('1.0', tk.END)

    for c in name_list:
        tkDisplay.insert(tk.END, c)
        tkDisplay.insert(tk.END,"\n")
    tkDisplay.config(state=tk.DISABLED)


window.mainloop()
