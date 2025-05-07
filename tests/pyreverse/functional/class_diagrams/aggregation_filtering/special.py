# Test for https://github.com/pylint-dev/pylint/issues/10373
# Aggregation relationships should be filtered according to attribute visibility

class P:
    def __init__(self, name: str = ""):
        self.name = name

class PublicAttr:
    def __init__(self):
        self.x: P = P("public")

class ProtectedAttr:
    def __init__(self):
        self._x: P = P("protected")

class PrivateAttr:
    def __init__(self):
        self.__x: P = P("private")

class SpecialAttr:
    def __init__(self):
        self.__x__: P = P("special")
