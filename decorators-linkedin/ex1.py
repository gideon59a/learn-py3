def fib_three(a, b, c):
    ''' Accept 3 numbers'''
    def get_three(d=0):
        '''Return the 3  numbers'''
        return a, b, c, 22+d
    return get_three

print(fib_three(1,1,2))
f = fib_three(1,1,2)
print(f())
print(f(8))
