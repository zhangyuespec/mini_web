class Line(object):
    def __init__(self, k, b):
        self.k = k
        self.b=b

    def __call__(self,x):
        print(self.k*x+self.b)

line=Line(1,2)
line(1)