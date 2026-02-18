import socket 

PORT = 587

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("0.0.0.0",PORT))
s.listen()
print(f"SERVER IS LISTENING ON PORT {PORT}")
client,addr = s.accept()

data = client.recv(1024)
if data:
    print(data)
else:
    print("packet lost..")