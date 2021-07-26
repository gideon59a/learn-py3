# per https://realpython.com/primer-on-python-decorators/
def say_hello(name):
    return f"Hello {name}"

def greet(funct):
    return funct("Bob")

#print(say_hello("Tom"))
#print(greet(say_hello))
#---------------------------------------

print("Basic decorator without parameters:")
def my_decorator(func):
    print("stam")
    def wrapper():
        print("Something is happening before the function is called.")
        func()
        print("Something is happening after the function is called.")
    print(f"wrapper ref:  {wrapper}")
    return wrapper  # !!! This line causes wrapper function to be returned (!), returned by my_decorator(say_whee)!!!

def say_whee():
    print("Whee!")


test = "orig"
if test == "orig":
    say_whee = my_decorator(say_whee)  # Returns the wrapper function!!!!!!!!!!!!!S
    print(f"say_whee ref: {say_whee}")
    print(say_whee())
else:
    say_whee_var = my_decorator(say_whee)   # Returns the wrapper function!!
    print(f"say_whee ref: {say_whee}")
    print(f"say_whee_var: {say_whee_var}")
    print(say_whee_var())
#---------------------------------------

print("\n\n With decorator syntax:")
def my_real_decorator(func):
    def wrapper():
        print("Something is REALLY happening before the function is called.")
        func()
        print("Something is REALLY happening after the function is called.")
    return wrapper

@my_real_decorator
def real_say_whee():
    print("Whee!")

real_say_whee()
#print("Real syntax:", real_say_whee())