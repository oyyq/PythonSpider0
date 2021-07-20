import socket

http_client = socket.socket()
http_client.connect(("127.0.0.1", 8000))
http_client.send('''''')


