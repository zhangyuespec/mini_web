import time
def set_func(func):
    def call_funct():
        start_time=time.time()
        func()
        stop_time=time.time()
        print("运行时间是%f"%(start_time-stop_time))
    return call_funct

@set_func
def test_1():
    print("----test1----")
    for i in range(1000):
        pass

test_1()