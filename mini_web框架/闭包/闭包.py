def line_1(k,b):
    def create_y(x):
        print(k*x+b)
    return create_y

line_1_1=line_1(1,2)#默认值是Ｎｏｎｅ
line_1_1(1)