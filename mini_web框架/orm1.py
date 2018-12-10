class ModelMetaClass(type):
    def __new__(cls, name, bases, attrs):
        mappings = dict()
        for k, v in attrs.items():
            if isinstance(v, tuple):
                mappings[k] = v

        for k in mappings.keys():
            attrs.pop(k)

        attrs['__mappings__'] = mappings
        attrs['__table__'] = name
        return type.__new__(cls,name,bases,attrs)

class User(metaclass=ModelMetaClass):
    uid=('uid',"int unsigned")
    name=('username',"barchar(30)")
    email=('email',"varchar(30)")
    password=('password',"varchar(30)")

    def __init__(self,**kwargs):
        for name,value in kwargs.items():
            setattr(self,name,value)

    def save(self):
            fields=[]
            args=[]
            for k,v in self.__mappings__.items():
                fields.append(v[0])
                args.append(getattr(self,k,None))

            args_temp=list()
            for temp in args:
                if isinstance(temp,int):
                    args_temp.append(str(temp))
                elif isinstance(temp,str):
                    args_temp.append("""'%s'"""%temp)

            sql='insert into %s (%s) values (%s)'%(self.__table__,','.join(fields),\
                                                   ','.join(str(i) for i in args_temp))
            print(sql)

u=User(uid=122,name="zhangyue",email="xxx",password="pass")
                                                                                                      
u.save()
