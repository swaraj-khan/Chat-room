import socket
import threading

def receive_messages():
    while True:
        message = client_socket.recv(1024).decode()
        print(f"Received message: {message}")

def send_messages():
    username = input("Enter your username: ")
    client_socket.send(username.encode())

    while True:
        message = input()
        formatted_message = f"{username}: {message}"
        client_socket.send(formatted_message.encode())
        if message == "exit":
            break

    client_socket.close()

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(("localhost", 9999))

receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()

send_thread = threading.Thread(target=send_messages)
send_thread.start()
