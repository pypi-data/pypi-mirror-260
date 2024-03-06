"""Message And Command OUT object."""
from copy import deepcopy

class Madout():
    def __init__(self, successvalue=True, message="", *args):
        self.successvalue = successvalue
        self.message = message
        self.data = args

    def __bool__(self):
        return self.successvalue

    def __str__(self):
        return self.message

    def __repr__(self):
        return ("<" + ("Successful" if self else "Failed") +
                " Madout object with text '" + self.message +
                f"' and {len(self.data)} output(s).>")

    def __getitem__(self, item):
        return self.data[item]

    def p(self):
        print(self.message)
        for dto in filter(lambda x: type(x) is Madout, self.data):
            print(dto.message)

    def addtext(self, other):
        cpy = deepcopy(self)
        if type(other) is Madout:
            cpy.message += (' ' + other.message)
        elif type(other) is str:
            cpy.message += (' ' + other)
        return cpy

    def append(self, other):
        self.data = (*self.data, other)

    def result(self):
        if self.data==():
            return ()
        return self.data[0]


class Madgood(Madout):
    def __init__(self):
        super().__init__(True, "")

    def __repr__(self):
        return "<Successful Madgood object.>"