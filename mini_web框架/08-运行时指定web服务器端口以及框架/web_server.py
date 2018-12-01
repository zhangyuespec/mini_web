import socket
import re
import multiprocessing
import time
import test
import sys


class WSGIserver(object):

    def __init__(self,port,app):
        # 1. 创建套接字
        self.tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcp_server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # 2. 绑定
        self.tcp_server_socket.bind(("172.16.70.64", port))

        # 3. 变为监听套接字
        self.tcp_server_socket.listen(128)

        self.application=app

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

            env=dict()#空字典
            env['PATH_INFO']=file_name
            body=self.application(env,self.set_response_header) #接耦合

            # 如果是已.py结尾那么就认为是动态请求
            header = "HTTP/1.1 200 OK %s\r\n"%self.status

            for temp in self.headers:
                header+="%s:%s\r\n"%(temp[0],temp[1])

            header += "\r\n"

            response=header+body

            new_socket.send(response.encode("utf-8"))

        # 关闭套接
        new_socket.close()

    def set_response_header(self,status ,headers):
        self.status=status
        self.headers=[('server','mini_web')]
        self.headers+=headers

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
    if  len(sys.argv)==3:
        try:
            port=int(sys.argv[1])
            frame_app_name=sys.argv[2]
        except Exception as ret:
            print("端口输入错误")
            return
    else:
        print("请按照一下方式运行：")
        print("python3 xxx.py 7890 test:application")
        return

    ret=re.match(r"([^:]+):(.*)",frame_app_name)
    if ret:
        frame_name=ret.group(1)
        app_name=ret.group(2)
    else:
        print("请按照一下方式运行：")
        print("python3 xxx.py 7890 test:application")
        return
    frame=__import__(frame_name)#返回值标记着导入的这个模板
    app=getattr(frame,app_name)
    #此时app就指向了框架中application这个函数





    wsgi_server = WSGIserver(frame,app)
    wsgi_server.runforever()


if __name__ == "__main__":
    main()
