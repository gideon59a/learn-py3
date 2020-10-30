
class Length:
    ''' from https://www.python-course.eu/python3_magic_methods '''
    __metric = {"mm": 0.001, "cm": 0.01, "m": 1, "km": 1000,
                "in": 0.0254, "ft": 0.3048, "yd": 0.9144,
                "mi": 1609.344}

    def __init__(self, value, unit="m"):
        self.value = value
        self.unit = unit

    def Converse2Metres(self):
        return self.value * Length.__metric[self.unit]

    def __add__(self, other):
        l = self.Converse2Metres() + other.Converse2Metres()
        return Length(l / Length.__metric[self.unit], self.unit)

    def __str__(self):  # ***** This is used e.g. for "print(x)"  *****
        return str(self.Converse2Metres())

    def __repr__(self):
        return "Length(" + str(self.value) + ", '" + self.unit + "')"

class Regular():
    a0=10
    b0=11

    def __init__(self, a, b):
        self.a = a
        self.b = b

    def f(self):
        return self.a + self.b

if __name__ == "__main__":

    regular = Regular(2,3)
    print(regular)

    x = Length(4)
    print(x)
    y = eval(repr(x))

    z = Length(4.5, "yd") + Length(1)
    print(repr(z))
    print(z)