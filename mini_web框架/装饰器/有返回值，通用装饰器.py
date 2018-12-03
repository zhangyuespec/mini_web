def set_func(func):
    print("开启装饰器")
    def call_func(*args,**kwargs):
        print("11111")
        print("22222")
        return func(*args,**kwargs)
    return  call_func

@set_func
def test(num,*args,**kwargs):
    print("test---%d"%num)
    print("test---",args)
    print("test---",kwargs)
    return "OK"

@set_func
def a():
    pass

ret = test(100)
print(ret)

ret2=a()
print(ret2)

