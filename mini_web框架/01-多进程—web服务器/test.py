import socket
import re
import multiprocessing

def server_client(new_socket):
    request = new_socket.recv(1024).decode("utf-8")

    request_line = request.splitlines()
    print("")
    print(">"*20)
    print(request_line)

    file_name=""
    ret=re.match(r"[^/]+(/[^ ]*)", request_line[0])

    if ret:
        file_name=ret.group(1)
        if file_name=="/":
            file_name="/index.html"

    try:
        f=open("./html"+file_name,"rb")

    except:
        response="HTTP/1.1 404 NOT FOUND \r\n"
        response+="\r\n"
        response+="----file not found----"
        new_socket.send(response.encode("utf-8"))

    else:
        html_content = f.read()
        f.close()
        response="HTTP/1.1 200 OK\r\n"
        response+="\r\n"

        new_socket.send(response.encode("utf-8"))

        new_socket.send(html_content)

    new_socket.close()


def main():
    # 创建套接字
    tcp_server_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    tcp_server_socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)#为了防止四次挥手失效

    #绑定
    tcp_server_socket.bind(("172.16.70.64",7080))

    #变为监听套接字
    tcp_server_socket.listen(128)

    while True:
        # 等待客户端链接
        new_socket,client_addr=tcp_server_socket.accept()

        #开启进程
        p=multiprocessing.Process(target=server_client,args=(new_socket,))

        p.start()
        new_socket.close()

    tcp_server_socket.close()

if __name__ == '__main__':
    main()

