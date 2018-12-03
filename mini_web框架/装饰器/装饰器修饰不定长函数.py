def set_func(func):
    print("开启装饰器")
    def call_func(*args,**kwargs):
        print("11111")
        print("22222")
        func(*args,**kwargs)
    return  call_func

@set_func
def test(num,*args,**kwargs):
    print("test---%d"%num)
    print("test---",args)
    print("test---",kwargs)

test(100)
test(100,200)
test(100,200,300,mm=500)