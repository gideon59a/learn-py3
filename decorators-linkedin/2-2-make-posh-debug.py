## with decorators

from functools import wraps

def make_posh(func):
    '''This is the function decorator'''
    @wraps(func)
    def wrapper():
        '''This is the wrapper function'''
        print("+---------+")
        print("|         |")
        result = func()
        print(result)
        print("|         |")
        print("+=========+")
        return result
    ## If the wrapper decorator was not used, then to see the proper metadata one should have added the following:
    #wrapper.__name__ = func.__name__
    #wrapper.__doc__ = func.__doc__
    return wrapper

@make_posh
def printfib():
    '''Print out Fibonacci'''
    return ' Fibonacci '


printfib()
print(printfib.__name__)
print(printfib.__doc__)
help(printfib)
