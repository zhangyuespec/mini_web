class Test(object):
    def __init__(self,func):
        self.func=func

    def __call__(self, *args, **kwargs):
        print("这里是装饰器添加的功能")
        return self.func()

@Test
def get_str():
    return "zhadf"

print(get_str())