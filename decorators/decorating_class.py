# per https://www.geeksforgeeks.org/class-as-decorator-in-python/
# Python program showing
# class decorator with *args
# and **kwargs

class MyDecorator:
    def __init__(self, function):
        self.function = function

    def __call__(self, *args, **kwargs):
        # We can add some code
        # before function call
        print("before")

        self.function(*args, **kwargs)

        # We can also add some code
        # after function call.v
        print("after")

        return "This is the return string"

# adding class decorator to the function
@MyDecorator
def function(name, message='Hello'):
    print("{}, {}".format(message, name))


return_value = function("geeks_for_geeks", "hellooo")
print(f"return_value: {return_value}")