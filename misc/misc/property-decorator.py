# REFs:
#     https://www.programiz.com/python-programming/property


# Basic method of setting and getting attributes in Python
class Celsiusa:
    def __init__(self, temperature=0):
        self.temperature = temperature

    def to_fahrenheit(self):
        return (self.temperature * 1.8) + 32


# Create a new object
#human = Celsiusa()

# Set the temperature
#human.temperature = 37

# Get the temperature attribute
#print(human.temperature)

# Get the to_fahrenheit method
#print(human.to_fahrenheit())

#print("__dict__: ", human.__dict__)

class Celsiusb:
    def __init__(self, temperature=0):
        self.set_temperature(temperature)

    def to_fahrenheit(self):
        return (self.get_temperature() * 1.8) + 32

    # getter method
    def get_temperature(self):
        return self._temperature

    # setter method
    def set_temperature(self, value):
        if value < -273.15:
            raise ValueError("Temperature below -273.15 is not possible.")
        self._temperature = value

#te = Celsiusb(-500)
print("end")
##################################################

# using property class
class Celsius:
    def __init__(self, temper=0):
        self.temperature = temper

    def to_fahrenheit(self):
        return (self.temperature * 1.8) + 32

    # getter
    def get_temperature(self):
        print("Getting value...")
        return self._temperature

    # setter
    def set_temperature(self, value):
        print("Setting value...")
        if value < -273.15:
            raise ValueError("Temperature below -273.15 is not possible")
        self._temperature = value

    # creating a property object
    # temperature = property(get_temperature, set_temperature)
    # make empty property
    temperature = property()
    print(temperature)
    # assign fget
    temperature = temperature.getter(get_temperature)
    print(temperature)
    # assign fset
    temperature = temperature.setter(set_temperature)
    print(temperature)

human = Celsius(37)
print(human.temperature)
print(human.to_fahrenheit())
human.temperature = -200

#h2 = Celsius(-3700)

print("end-----------------------")

# Using @property decorator
class Celsiusc:
    def __init__(self, temperature=0):
        self.temperature = temperature

    def to_fahrenheit(self):
        return (self.temperature * 1.8) + 32

    @property
    def temperature(self):
        print("Getting value...")
        return self._temperature

    @temperature.setter
    def temperature(self, value):
        print("Setting value...")
        if value < -273.15:
            raise ValueError("Temperature below -273 is not possible")
        self._temperature = value


# create an object
humanc = Celsiusc(37)

print(humanc.temperature)

print(humanc.to_fahrenheit())

coldest_thing = Celsiusc(-30)