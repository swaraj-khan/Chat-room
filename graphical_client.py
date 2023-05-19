import socket
import threading
import tkinter as tk

def receive_messages():
    while True:
        message = client_socket.recv(1024).decode()
        chat_box.configure(state="normal")  # Enable editing temporarily
        chat_box.insert(tk.END, message + "\n")
        chat_box.configure(state="disabled")  # Disable editing
        chat_box.see(tk.END)  # Scroll to the latest message

def send_message():
    if not username:
        set_username()
        return

    message = message_entry.get()
    formatted_message = f"{username}: {message}"
    client_socket.send(formatted_message.encode())
    if message == "exit":
        client_socket.close()
        window.quit()
    message_entry.delete(0, tk.END)

def set_username():
    global username
    username = username_entry.get()
    username_entry.configure(state="disabled")
    start_button.configure(state="disabled")
    message_entry.configure(state="normal")
    send_button.configure(state="normal")
    message_entry.focus_set()

def on_closing():
    client_socket.send("exit".encode())
    client_socket.close()
    window.quit()

# Create the GUI window
window = tk.Tk()
window.title("Chatroom")

# Create chat box
chat_box = tk.Text(window, height=10, width=50, state="disabled")
chat_box.pack()

# Create username entry field
username_entry = tk.Entry(window, width=20)
username_entry.pack()

# Create start button
start_button = tk.Button(window, text="Start", command=set_username)
start_button.pack()

# Create message entry field
message_entry = tk.Entry(window, width=40, state="disabled")
message_entry.pack()

# Create send button
send_button = tk.Button(window, text="Send", command=send_message, state="disabled")
send_button.pack()

# Set up the client socket and threads
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(("localhost", 9999))

receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()

# Configure closing event
window.protocol("WM_DELETE_WINDOW", on_closing)

# Global variable for username
username = ""

# Start the GUI event loop
window.mainloop()
