def set_func(func):
    def call_funct(num):
        print("－－－这是权限验证１－－－")
        print("---这是权限验证２——————")
        func(num)
    return call_funct

@set_func
def test_1(num):
    print("----test1----%d"%num)

test_1(10000)