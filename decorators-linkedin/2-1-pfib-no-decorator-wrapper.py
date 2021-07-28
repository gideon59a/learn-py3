def my_decorator(func):
    '''Decorator function'''
    def wrapper():
        '''return string F-I-B-N-A-C-C-I '''
        return 'F-I-B-N-A-C-C-I'
    return wrapper

def pfib():
    '''Return Fibonacci'''
    return 'Fibonacci'

print(type(pfib), id(pfib), pfib())

pfib = my_decorator(pfib)  #!! change pfib, so it is decorated.

print(type(pfib), id(pfib), pfib)   # A different ID, and a ref to my_decorator.<locals>.wrapper !!
print(pfib())
