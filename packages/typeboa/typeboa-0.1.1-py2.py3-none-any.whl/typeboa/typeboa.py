class _CollectionType:
    def __init__(self, outer_type, inner_type) -> None:
        self.outer_type = outer_type
        self.inner_type = inner_type
        self.__name__ = f'{self.outer_type.__name__}[{self.inner_type.__name__}]'
    
    def __or__(self, other):
        if type(other) != self.outer_type:
            raise Exception(f'Expected type {self.outer_type.__name__}, got {type(other).__name__}')
        if self.inner_type is not None:
            for i in other:
                if not isinstance(i, self.inner_type):
                    raise Exception(f'Expected type {self.outer_type.__name__}[{self.inner_type.__name__}], got {self.outer_type.__name__}[{type(i).__name__}]')
        return other

    def __instancecheck__(self, other):
        if not isinstance(other, self.outer_type):
            return False
        if self.inner_type is not None:
            for i in other:
                if not isinstance(i, self.inner_type):
                    return False
        return True

class _DictType:
    def __init__(self, key_type, value_type) -> None:
        self.outer_type = dict
        self.key_type = key_type
        self.value_type = value_type
        self.__name__ = f'{self.outer_type.__name__}[{self.key_type.__name__}:{self.value_type.__name__}]'
    
    def __or__(self, other: dict):
        if type(other) != self.outer_type:
            raise Exception(f'Expected type {self.outer_type.__name__}, got {type(other).__name__}')
        if self.key_type is not None:
            for k, v in other.items():
                if (not isinstance(k, self.key_type)) or (not isinstance(v, self.value_type)):
                    raise Exception(f'Expected type {self.outer_type.__name__}[{self.key_type.__name__}:{self.value_type.__name__}], got {self.outer_type.__name__}[{type(k).__name__}:{type(v).__name__}]]')
        return other

    def __instancecheck__(self, other):
        if not isinstance(other, self.outer_type):
            return False
        if self.key_type is not None:
            for k, v in other.items():
                if (not isinstance(k, self.key_type)) or (not isinstance(v, self.value_type)):
                    return False
        return True

class _MetaType(type):
    def __or__(cls, other):
        # Here, cls refers to the class itself, not an instance
        if type(other) != cls.expected_type:
            raise Exception(f'Expected type {cls.expected_type.__name__}, got {type(other).__name__}')
        return other

    def __call__(cls, *args, **kwds):
        if isinstance(cls.expected_type, tuple):
            return cls.expected_type[-1](*args, **kwds)
        return cls.expected_type(*args, **kwds)

    def __eq__(cls, other):
        if isinstance(cls.expected_type, tuple):
            return any(other == i for i in cls.expected_type)
        return other == cls.expected_type

    def __instancecheck__(cls, instance):
        if isinstance(cls.expected_type, tuple):
            return any(isinstance(instance, i) for i in cls.expected_type)
        return isinstance(instance, cls.expected_type)

    def __getitem__(cls, target):
        if isinstance(target, slice):
            return _DictType(target.start, target.stop)
        return _CollectionType(cls.outer_type, target)
        

class Int(metaclass=_MetaType):
    expected_type = int

class Float(metaclass=_MetaType):
    expected_type = float

class Number(metaclass=_MetaType):
    expected_type = (int, float)

class Bool(metaclass=_MetaType):
    expected_type = bool

class Str(metaclass=_MetaType):
    expected_type = str

class List(metaclass=_MetaType):
    expected_type = list

class Set(metaclass=_MetaType):
    expected_type = set

class Tuple(metaclass=_MetaType):
    expected_type = tuple

class Dict(metaclass=_MetaType):
    expected_type = dict

def gen_type(t):
    class NewType(metaclass=_MetaType):
        expected_type = t
    return NewType
