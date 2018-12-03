def set_func(func):
    print("开启装饰器1111")
    def call_func():
        print("11111")
        return func()
    return  call_func

def add_qx(func):
    print("开启装饰器222")
    def call_func():
        print("222")
        return func()
    return  call_func


@set_func
@add_qx
def test():
    print("----test----")


test()


