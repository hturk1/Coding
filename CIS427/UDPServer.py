import socket
# Server configuration
HOST = "127.0.0.1"
PORT = 12345

# Create a UDP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((HOST, PORT))

print(f"UDP Server is listening on {HOST}:{PORT}")

while True:
    data, addr = server_socket.recvfrom(1024)  # Receive data from client
    print(f"Received message from {addr}: {data.decode()}")

    response = f"Hello Client, I received: {data.decode()}"
    server_socket.sendto(response.encode(), addr)  # Send response