def set_func(func):
    def call_funct():
        print("－－－这是权限验证１－－－")
        print("---这是权限验证２——————")

        func()
    return call_funct

#@set_func
def test_1():
    print("----test1----")

test_1 = set_func(test_1)
test_1()
#test_1()