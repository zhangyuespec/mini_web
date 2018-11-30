
def index():
    return "主页"

def login():
    return "登录"

def application(env,start_response):
    start_response("200 OK",[('Content-Type','text/html;charset=utf-8'),('server','my_web')])
    file_name=env['PATH_INFO']

    if file_name=="/index.py":
        return index()
    elif file_name == "/login.py":
        return login()
    else:

        return 'Hello World!我爱你中国'
