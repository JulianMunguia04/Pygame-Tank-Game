import socket
import pickle
import time
from dotenv import load_dotenv
import os

load_dotenv()
HOST = os.getenv("SERVER_HOST", "127.0.0.1")
PORT = int(os.getenv("SERVER_PORT", 5000))

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()
print(f"Server running on {HOST}:{PORT}")

while True:
    client, addr = server.accept()
    print(f"Connected to {addr}")
    try:
        data = client.recv(4096)
        if data:
            obj = pickle.loads(data)
            if obj.get("message") == "server-check":
                client.send(b"Server Received Message")
    except Exception as e:
        print("Error:", e)
    client.close()
