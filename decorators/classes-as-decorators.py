# from https://realpython.com/primer-on-python-decorators/#classes-as-decorators

# A NON DECORATOR CLASS EXAMPLE
class Counter:
    def __init__(self, start=0):
        print("Init\n")
        self.count = start

    def __call__(self):
        self.count += 1
        print(f"Current count is {self.count}")
        return 7

print("Instanciate:")
counter = Counter()

print("run:")
print(f"print: { counter() }\n" )

print("run:")
print(f"print: { counter() }\n" )

############################################################################################################
# A DECORATOR CLASS EXAMPLE
print("\nA DECORATOR CLASS EXAMPLE\n=========================\n")
import functools

class CountCalls:
    def __init__(self, func):
        print("Init")
        functools.update_wrapper(self, func)
        self.func = func
        self.num_calls = 0

    def __call__(self, *args, **kwargs):
        self.num_calls += 1
        print(f"Call {self.num_calls} of {self.func.__name__!r}")
        return self.func(*args, **kwargs)

@CountCalls
def say_whee():
    print("Whee!")

say_whee()
say_whee()