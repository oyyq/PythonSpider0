import socket
import json
import threading
server = socket.socket()
#绑定 到0.0.0.0:8000端口上
server.bind(('0.0.0.0', 8002))
server.listen()

# 1. 为什么说http协议是无状态的?
# 2. 一个网站如何识别一个请求属于哪个用户？
# 3. Cookie在http协议中就是一段文本信息，写在http协议的headers中
# 4. http协议是无状态的，每次http请求都会带上cookie (为什么不带上username & password?)



# 服务器在用户登录成功后，给用户返回一段字符串sessionid(够复杂，生成算法别人伪造不了，加密传输给用户)
# 每次用户请求的时候带上参数 username, password => 容易被劫持

user_info = {
    "sessionid": "oyyq"
}
# 浏览器每一次请求(所有url)都自动带上这个sessionid
# 1. 如何告知浏览器sessionid
#    以http响应格式返回，响应头Set-Cookie, Expires设定过期时间，浏览器如何识别并保存Cookie是另外一个课题
#    HTTP/1.0 200 OK
#    Content-type: text/html
#    Set-Cookie: name=bobby
#    Set-Cookie: course_id=78
#    Set-Cookie: sessionid=abc123; Expires=Wed, 09 Jun 2021 10:18:14 GMT
# 2. 如何确保浏览器每一次请求都带上这个sessionid
#       浏览器默认行为
# 3. session和cookie的区别？
#   1. session是由服务器维护的，并由服务器解释，通过Set-Cookie交给浏览器
#   2. cookie是浏览器的工具，并在后面的每一次请求中都带上这些值


def handle_sock(sock,addr):
    # recv方法是阻塞的
    tmp_data = sock.recv(1024)
    print(tmp_data.decode("utf8"))
    response_template = '''HTTP/1.1 200 OK
Content-Type: text/html
Set-Cookie: name=bobby
Set-Cookie: course_id=78
Set-Cookie: sessionid=abc123; Expires=Wed, 09 Jun 2022 10:18:14 GTM

{}

'''
    data = [
        {"name": "django打造在线教育",
         "teacher": "bobby",
         "url": "https://coding.imooc.com/class/78.html"
         }
    ]

    sock.send(response_template.format(json.dumps(data)).encode("utf8"))
    sock.close()



if __name__ =="__main__":
    while True:
        sock, addr = server.accept()
        thread = threading.Thread(target=handle_sock, args=(sock, addr))
        thread.start()