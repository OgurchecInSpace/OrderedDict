class OrderedDict:
    def __init__(self, get_object=None):
        self.order = []
        if get_object is not None:
            if isinstance(get_object, dict):
                for key, value in get_object.items():
                    self.order.append(key)
                    setattr(self, str(hash(key)), value)
            elif type(get_object) in (tuple, list) \
                    and all(map(lambda item: len(item) == 2 and type(item) in (list, tuple), get_object)):
                for key, value in get_object:
                    self.order.append(key)
                    setattr(self, str(hash(key)), value)
            else:
                raise TypeError(f"TypeError: {type(get_object)} object doesn't suit to convert to OrderedDict")

    def __setitem__(self, key, value):
        setattr(self, str(hash(key)), value)
        if key not in self.order:
            self.order.append(key)

    def __getitem__(self, key):
        return getattr(self, str(hash(key)))

    def __delitem__(self, key):
        delattr(self, str(hash(key)))
        del self.order[self.order.index(key)]

    def __str__(self):
        return '{' + ', '.join(f'{key}: {getattr(self, str(hash(key)))}' for key in self.order) + '}'

    def __len__(self):
        return len(self.order)

    def __iter__(self):
        return iter(self.order)

    def get(self, key, default=None):
        if key in self.order:
            return getattr(self, str(hash(key)))
        else:
            return default

    def keys(self):
        return iter(self.order)

    def values(self):
        return iter(getattr(self, str(hash(key))) for key in self.order)

    def items(self):
        return iter((key, getattr(self, str(hash(key)))) for key in self.order)

    def clear(self):
        for key in self.order:
            delattr(self, str(hash(key)))
        self.order = []

    def copy(self):
        new_order_dict = OrderedDict()
        new_order_dict.order = self.order.copy()
        for key, value in self.items():
            setattr(new_order_dict, str(hash(key)), value)
        return new_order_dict

    def pop(self, key, default=None):
        if key in self.order:
            value = getattr(self, str(hash(key)))
            delattr(self, str(hash(key)))
            self.order.remove(key)
            return value
        else:
            return default

    def popitem(self):
        return self.order[-1], getattr(self, str(hash(self.order[-1])))

    def setdefault(self, key, value):
        if key in self.order:
            return getattr(self, str(hash(key)))
        else:
            self.order.append(key)
            setattr(self, str(hash(key)), value)
            return value

    def update(self, iterable):
        if isinstance(iterable, OrderedDict):
            new_ordered_dict = iterable
        else:
            new_ordered_dict = OrderedDict(iterable)
        for key, value in new_ordered_dict.items():
            if key not in self.order:
                self.order.append(key)
            setattr(self, str(hash(key)), value)

    @staticmethod
    def fromkeys(keys, value=None):
        return OrderedDict({key: value for key in keys})

