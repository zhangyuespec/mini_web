def set_level(level_num):
    def set_func(func):
        def call_func(*args, **kwargs):
            # level = args[0]
            if level_num == 1:
                print("权限验证１")
            elif level_num == 2:
                print("权限验证２")
            return func()

        return call_func

    return set_func


@set_level(1)
def test1():
    print("test1")
    return "OK"


@set_level(2)
def test2():
    print("test2")
    return "OK"


test1()
test2()
