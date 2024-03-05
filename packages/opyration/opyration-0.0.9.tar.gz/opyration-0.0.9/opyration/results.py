from collections import deque


class Lookup(object):
    def __init__(self, data: dict):
        self._data = data

    def __getattr__(self, key: str):
        value = self._data.get(key)
        if isinstance(value, dict):
            return Lookup(value)
        return value


class Results(object):
    def __init__(self, data: list):
        self.__data = deque(data)
    
    def __bool__(self):
        return bool(self.__data)

    def next(self):
        try: return self.__data.popleft()
        except: return None

    def last(self):
        try: return self.__data.pop()
        except: return None

    def pop(self):
        datum = self.next()
        if not datum: return None
        return Lookup(datum)
