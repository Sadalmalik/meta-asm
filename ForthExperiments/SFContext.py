class Context:
    def __init__(self, parent=None):
        self.parent = parent
        self._container = {}

    def __setitem__(self, key, value):
        self._container[key] = value

    def __getitem__(self, key):
        if key in self._container:
            return self._container[key]
        elif self.parent is not None:
            return self.parent[key]
        else:
            raise KeyError(key)
