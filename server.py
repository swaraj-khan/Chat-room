import socket
import threading

def handle_client(client_socket, client_address):
    while True:
        message = client_socket.recv(1024).decode()
        if message == "exit":
            break
        print(f"Received message from {client_address}: {message}")
        broadcast_message(message)

    client_socket.close()
    print(f"Connection with {client_address} closed.")

def broadcast_message(message):
    for client_socket in client_sockets:
        client_socket.send(message.encode())

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("localhost", 9999))
    server_socket.listen(5)

    print("Server started. Listening for connections...")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"New connection from {client_address}")
        client_sockets.append(client_socket)

        threading.Thread(target=handle_client, args=(client_socket, client_address)).start()

    server_socket.close()

client_sockets = []

start_server()
