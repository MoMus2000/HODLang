class Environment:
    def __init__(self):
        self.mapper = {}

    def define(self, key, value):
        self.mapper[key] = value

    def get(self, key):
        if key not in self.mapper:
            raise Exception("VAR Not Found !")
        return self.mapper[key]

