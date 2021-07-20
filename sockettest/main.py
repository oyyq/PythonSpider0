import json
import socket
import threading


def handle_sock(sock, addr):
    while True:
        tmp_data = sock.recv(1024)
        tmp_data = tmp_data.decode("utf8")
        request_line = tmp_data.splitlines()[0]     #按" "划分
        if request_line:
            method = request_line.split()[0]
            path = request_line.split()[1]          #form action = "/", 表单提交到path
            if method == "GET":
                response_template = '''HTTP/1.1 200 OK
                
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
    <form action="/" method="POST">
    <input type="text" name="name"/>
    <input type="password" name="password"/>
    <input type="submit" value="登陆"/>
    </form>
</body>
</html>

'''
                sendN = sock.send(response_template.encode("utf8"))
                print(sendN)
                #sock.close()
            elif method == "POST":
                response_template = '''HTTP/1.1 200 OK
                Content-Type: application/json
                
                {}
                
                '''
                data = [
                    {
                        "name": "scrapy分布式爬虫",
                        "teacher": "bobby",
                        "url":"https://coding.imooc.com/class/92.html"
                    },
                    {
                        "name":"django rest framework",
                        "teacher":"bobby",
                        "url":"https://coding.imooc.com/class/131.html"
                    },
                    {
                        "name":"tornado",
                        "teacher":"bobby",
                        "url":"https://coding.imooc.com/class/290.html"
                    },
                ]
                sock.send(response_template.format(json.dumps(data)).encode("utf8"))
                #sock.close()
                break


if __name__ == "__main__":
    server_sock = socket.socket()
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_sock.bind(('0.0.0.0', 8000))
    server_sock.listen()
    while True:
        sock, addr = server_sock.accept()
        thread = threading.Thread(target=handle_sock, args=(sock, addr))
        thread.start()
