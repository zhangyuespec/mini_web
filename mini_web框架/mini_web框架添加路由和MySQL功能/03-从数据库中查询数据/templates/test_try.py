import socket
import re
import multiprocessing
import sys

class WSGIServer(object):
    def __init__(self,port,app,static_path):
        self.tcp_server_scoket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.tcp_server_scoket.setsockopt(socket.SOL_SOCKET)
        self.tcp_server_scoket.bind(("",port))
        self.tcp_server_scoket.listen(128)
        self.application=app
        self.static_path=static_path

    def server_client(self,new_scoket):
        request=new_scoket.recv(1024).decode("utf-8")
        request_lines=request.splitlines()
        print("")
        print(">"*20)
        print(request_lines)

        file_name=""
        ret=re.match(r"[^/]+(/[^ ]*)",request_lines[0])
        if ret:
            file_name=ret.group(1)
            if file_name=="/":
                file_name="/index.html"

        if not file_name.endswith(".py"):
            try:
                f=open(self.static_path+file_name,"rb")
            except:
                response="HTTP/1.1 404 NOT FOUND\r\n"
                response+="\r\n"
                response+="----file not found-----"
                new_scoket.send(response.encode("utf-8"))
            else:
                html_content=f.read()
                f.close()
                response="HTTP/1.1 200 OK\r\n"
                response+="\r\n"
                new_scoket.send(response.encode("utf-8"))
                new_scoket.send(html_content)
        else:
            env=dict()
            env['PATH_INFO']=file_name
            body=self.application(env,self.set_response_header)
            header="HTTP/1.1 %s\r\n"%self.status

            for temp in self.headers:
                header+="%s:%s"%(temp[0],temp[1])

            header+="\r\n"

            response=header+body

            new_scoket.send(response.encode("utf-8"))

        new_scoket.close()


    def set_response_header(self,status,headers):
        self.status=status
        self.headers=[("server","mini_web v8.8")]
        self.headers+=headers

    def run_forever(self):
        while True:
            new_socket,client_addr=self.tcp_server_scoket.accept()

            p=multiprocessing.Process(target=self.server_client,args=(new_socket,))
            p.start()

            new_socket.close()

        self.tcp_server_scoket.close()


def main():
    if len(sys.argv)==3:
        try:
            port=int(sys.argv[1])
            frame_app_name=sys.argv[2]
        except Exception as ret:
            print("ｐｏｒｔ有错")
            return

    else:
        print("请按照以下方式运行:")
        print("python3 xxxx.py 7890 mini_frame:application")
        return
    ret=re.match(r"([^:]+):(.*)",frame_app_name)
    if ret:
        frame_name=ret.group(1)
        app_name=ret.group(2)

    else:
        print("请按照python3 xxxx.py 7890 mini_frame:application运行")
        return

    with open("./web_server.conf") as f:
        conf_info=eval(f.read())

    sys.path.append(conf_info['dynamic_path'])

    frame=__import__(frame_name)
    app=getattr(frame,app_name)

    wsgi_server=WSGIServer(port,app,conf_info['static_name'])
    wsgi_server.run_forever()

if __name__=="__main__":
    main()