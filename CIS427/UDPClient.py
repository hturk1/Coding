import socket

# Server details
SERVER_HOST = "127.0.0.1"
SERVER_PORT = 12345

# Create a UDP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

message = "Hello, UDP Server!"
client_socket.sendto(message.encode(), (SERVER_HOST, SERVER_PORT))  # Send message to server

data, _ = client_socket.recvfrom(1024)  # Receive response from server
print(f"Server replied: {data.decode()}")

client_socket.close()