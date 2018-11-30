import time

def login():
    return "welcome to our website ----time is %s "%time.time()

def register():
    return "登录"

def profile():
    return "个人主页"

def application(file_name):
    if file_name=="/log_in.py":
        login()
    elif file_name=="/register.py":
        register()
    elif file_name=="/profile.py":
        profile()
    else:
        return "没有发现你的主页"
