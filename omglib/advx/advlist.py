from typing import *
NoneType=type(None)

class _Listify:
    class _LEN:
        def __init__(self):
            super().__init__()
        def __gt__(self,ot):
            return len(ot)
        def __lt__(self,ot):
            return len(ot)
        def __call__(self, single):
            return len(single)
        def __getitem__(self,item):
            return len(item)
    class _SUM:
        def __init__(self):
            super().__init__()
        def __gt__(self,ot):
            return sum(ot)
        def __lt__(self,ot):
            return sum(ot)
        def __call__(self, single):
            return sum(single)
        def __getitem__(self,item):
            return sum(item)
    class _SET:
        def __init__(self):
            super().__init__()
        def __gt__(self,ot):
            return set(ot)
        def __lt__(self,ot):
            return set(ot)
        def __call__(self, single):
            return set(single)
        def __getitem__(self,item):
            return set(item)
    class _TUPLE:
        def __init__(self):
            super().__init__()
        def __gt__(self,ot):
            return tuple(ot)
        def __lt__(self,ot):
            return tuple(ot)
        def __call__(self, single):
            return tuple(single)
        def __getitem__(self,item):
            return tuple(item)
    class _SORT:
        def __init__(self):
            super().__init__()
        def __gt__(self,ot):
            return sorted(ot)
        def __lt__(self,ot):
            return sorted(ot)
        def __call__(self, single):
            return sorted(single)
        def __getitem__(self,item):
            return sorted(item)
    
    LEN = _LEN()
    L = _LEN()
    SUM = _SUM()
    SM = _SUM()
    SET = _SET()
    SX = _SET()
    TUPLE = _TUPLE()
    T = _TUPLE()
    SORT = _SORT()
    S = _SORT()
    def __init__(self):
        self.__LAST_OP = []
    def __gt__(self,ot):
        if type(ot) in [int,float,complex,NoneType,bool]:
            self.__LAST_OP = list([ot])
            return self.__LAST_OP
        elif type(ot) == dict:
            self.__LAST_OP = list(ot.keys())
            return self.__LAST_OP
        self.__LAST_OP = list(ot)
        return self.__LAST_OP
    def __lt__(self,ot):
        if type(ot) in [int,float,complex,NoneType,bool]:
            self.__LAST_OP = list([ot])
            return self.__LAST_OP
        elif type(ot) == dict:
            self.__LAST_OP = list(ot.values())
            return self.__LAST_OP
        self.__LAST_OP = list(ot)
        return self.__LAST_OP
    def new(self,optional_value:Optional[Any]=None):
        if not optional_value:
            pointer = _Listify()
            pointer.__LAST_OP = self.__LAST_OP
            return pointer
        pointer = _Listify()
        pointer.__LAST_OP = self.__gt__(optional_value)
        return pointer
    def n(self,optional_value:Optional[Any]=None):
        return self.new(optional_value=optional_value)
    def __getitem__(self,it):
        return self.__LAST_OP[it]
    @property
    def v(self):return self.__LAST_OP
    @property
    def r(self):self.__LAST_OP = [];return self
    def __call__(self, *args, **kwds):
        if args:
            return self.new(args)
        return _Listify()
    @property
    def totuple(self):
        return tuple(self.__LAST_OP)
    @property
    def tuple(self):
        return tuple(self.__LAST_OP)
    @property
    def set(self):
        return set(self.__LAST_OP)
    @property
    def toset(self):
        return set(self.__LAST_OP)
    @property
    def sum(self):
        return sum(self.__LAST_OP)
    def addItem(self,item:Any):
        self.__LAST_OP.append(item)
        return self
    def append(self,item:Any):
        return self.addItem(item)
    def remove(self,value:Any):
        self.__LAST_OP.remove(value)
        return self
    def clear(self):self.__LAST_OP.clear();return self
    def copy(self):return self.new(self.__LAST_OP)
    def index(self,value,start=0,stop=9223372036854775807):return self.__LAST_OP.index(value,start,stop)
    def count(self,value:Any):return self.__LAST_OP.count(value)
    def length(self):return len(self.__LAST_OP)
    def len(self):return self.length()
    def extend(self,iterable:Iterable):self.__LAST_OP.extend(iterable);return self
    def pop(self,index=-1):return self.pop(index)
    def insert(self,index,object):self.__LAST_OP.insert(index,object);return self

