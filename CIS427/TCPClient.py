import socket
import sys #needed for command-line if I am not mistaken

#server details
SERVER_HOST = sys.argv[1] #take ip from command line
SERVER_PORT = 12345

#create a TCP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((SERVER_HOST, SERVER_PORT))  #connect to server

while True: 
    #take data as input from user
    message = input("Choose command (MSGGET, MSGSTORE, QUIT, SHUTDOWN): ").strip() #give option to user
    client_socket.sendall(f"{message}\n".encode()) #send chose to server

    #handle MSGGET if chosen
    if message == "MSGGET":
        data = client_socket.recv(1024).decode()
        print(f"Server: {data}")
    
    #handle MSGSTORE if chosen
    elif message == "MSGSTORE":
        data = client_socket.recv(1024).decode()
        print(f"Server: {data}")
        message2 = input("What should be the new motd: ").strip() #update message of the day
        client_socket.sendall(f"{message2}\n".encode())
        data = client_socket.recv(1024).decode()
        print(f"Server: {data}")
    
    #handle QUIT if chosen
    elif message == "QUIT":
        data = client_socket.recv(1024).decode()
        print(f"Server: {data}")
        break #break out to end connection

    #handle SHUTDOWN if chosen
    elif message == "SHUTDOWN":
        data = client_socket.recv(1024).decode().strip() #need to strip or else causes errors
        print(f"Server: {data}")
        if data == "300 PASSWORD REQUIRED": #asking for password
            password = input("Enter password: ").strip()
            client_socket.sendall(f"{password}\n".encode())
            data = client_socket.recv(1024).decode().strip()
            print(f"Server: {data}")
            if data == "200 OK": #if correct password
                break  #break out to end connection
            elif data == "301 WRONG PASSWORD": #if incorrect password
                print("Incorrect password...")

client_socket.close()