x=300
def test_1():
    x=200
    def test_2():
        nonlocal  x
        print("----1----X=%d"%x)
        x = 100
        print("----2----X=%d"%x)
    return test_2

t=test_1()
t()