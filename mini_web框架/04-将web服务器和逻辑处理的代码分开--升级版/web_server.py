import socket
import re
import multiprocessing
import time
import test


class WSGIserver(object):

    def __init__(self):
        # 1. 创建套接字
        self.tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcp_server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # 2. 绑定
        self.tcp_server_socket.bind(("172.16.70.64", 7890))

        # 3. 变为监听套接字
        self.tcp_server_socket.listen(128)

    def service_client(self, new_socket):
        """为这个客户端返回数据"""

        # 1. 接收浏览器发送过来的请求 ，即http请求
        # GET / HTTP/1.1
        # .....
        request = new_socket.recv(1024).decode("utf-8")
        # print(">>>"*50)
        # print(request)

        request_lines = request.splitlines()
        print("")
        print(">" * 20)
        print(request_lines)

        # GET /index.html HTTP/1.1
        # get post put del
        file_name = ""
        ret = re.match(r"[^/]+(/[^ ]*)", request_lines[0])
        if ret:
            file_name = ret.group(1)
            # print("*"*50, file_name)
            if file_name == "/":
                file_name = "/index.html"

        # 2. 返回http格式的数据，给浏览器
        # 如果请求的资源不是.py结尾的就认为是静态资源
        if not file_name.endswith(".py"):
            try:
                f = open("../html" + file_name, "rb")
            except:
                response = "HTTP/1.1 404 NOT FOUND\r\n"
                response += "\r\n"
                response += "------file not found-----"
                new_socket.send(response.encode("utf-8"))
            else:
                html_content = f.read()
                f.close()
                # 2.1 准备发送给浏览器的数据---header
                response = "HTTP/1.1 200 OK\r\n"
                response += "\r\n"
                # 2.2 准备发送给浏览器的数据---boy
                # response += "hahahhah"

                # 将response header发送给浏览器
                new_socket.send(response.encode("utf-8"))
                # 将response body发送给浏览器
                new_socket.send(html_content)
        else:
            # 如果是已.py结尾那么就认为是动态请求
            header="HTTP/1.1 200 OK\r\n"
            header+="\r\n"

            #body="江姗姗哟%s"%time.ctime()
            body=test.application(file_name) #接耦合
            #body=test.login()

            response=header+body

            new_socket.send(response.encode("utf-8"))

        # 关闭套接
        new_socket.close()

    def runforever(self):
        """用来完成整体的控制"""

        while True:
            # 4. 等待新客户端的链接
            new_socket, client_addr = self.tcp_server_socket.accept()

            # 开一个进程
            p = multiprocessing.Process(target=self.service_client, args=(new_socket,))

            p.start()

            new_socket.close()

            # # 5. 为这个客户端服务
            # service_client(new_socket)

        # 关闭监听套接字
        tcp_server_socket.close()


def main():
    """
    控制整体，创建一个web服务器对象，然后调用这个对象的run方法
    :return:None
    """
    wsgi_server = WSGIserver()
    wsgi_server.runforever()


if __name__ == "__main__":
    main()
