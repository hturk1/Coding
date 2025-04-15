import socket

#server configuration
HOST = "127.0.0.1"
PORT = 12345

#create a TCP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(5)

defaultMessage = "An apple a day keeps the doctor away." #initialize default message
Password = "123!abc" #initialize password
todaysMessage = defaultMessage 
waitingForStore = False #flag for storing message

print(f"TCP Server is listening on {HOST}:{PORT}")

conn, addr = server_socket.accept()  #accept connection from client
print(f"Connected by {addr}")

while True:

    data = conn.recv(1024).decode().strip() #receive data
    print(f"Received from {addr}: {data}") #show that server is receiving data

    #handle MSGGET
    if data == "MSGGET":
        conn.sendall("200 OK\n".encode())
        conn.sendall(f"{todaysMessage}\n".encode())

    #handle MSGSTORE
    elif data == "MSGSTORE":
        conn.sendall("200 OK\n".encode())
        waitingForStore = True #change flag to so you can update message
    elif waitingForStore:
        todaysMessage = data #store new message from user
        conn.sendall("200 OK\n".encode())
        waitingForStore = False #change flag back 

    #handle QUIT
    elif data == "QUIT":
        conn.sendall("200 OK\n".encode())
        break  #break out to close connection

    #handle SHUTDOWN
    elif data == "SHUTDOWN":
        conn.sendall("300 PASSWORD REQUIRED\n".encode())
        password = conn.recv(1024).decode().strip()
        if password == Password: #if given password is same as default
            conn.sendall("200 OK\n".encode())
            break  #break out to close connection
        else:
            conn.sendall("301 WRONG PASSWORD\n".encode()) #if given passedword is not same as default

#close connection
conn.close()
server_socket.close()
