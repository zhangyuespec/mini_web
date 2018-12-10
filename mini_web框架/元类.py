class UpperAttrMetaClass(type):
    def __new__(cls, class_name,class_parents,class_attr):
        new_attr={}
        for name,value in class_attr.items():
            if not name.startswith("__"):
                new_attr[name.upper()]=value

        return type(class_name,class_parents,new_attr)


class Foo(object,metaclass=UpperAttrMetaClass):
    bar="bip"

print(hasattr(Foo,"bar"))

print(hasattr(Foo,"BAR"))

f=Foo()
print(f.BAR)


class Singleton(object):
    __instance = None
    __first_init = True

    def __init__(self, name, age):
        if self.__first_init:
            self.name = name
            self.age = age
            self.__first_init = False

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = object.__new__(cls)
        return cls.__instance


a = Singleton('a', 12)
b = Singleton('b', 13)
print(a)
print(b)

print(a.name)
print(b.name)
print(b._Singleton__first_init)