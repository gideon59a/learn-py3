def scope_test():
    return
    def do_local():
        spam = "local spam"

    def do_nonlocal():
        nonlocal spam
        spam = "nonlocal spam"

    def do_global():
        global spam
        spam = "global spam"

    spam = "test spam"
    do_local()
    print("After local assignment:", spam)
    do_nonlocal()
    print("After nonlocal assignment:", spam)
    do_global()
    print("After global assignment:", spam)

#scope_test()
#print("In global scope:", spam)



class MyClass:
    """A simple example class"""
    i = 12345

    def f(self):
        return 'hello world'

x = MyClass()
print(type(x))
x.counter = 1
while x.counter < 10:
    x.counter = x.counter * 2
print(x.counter)
del x.counter

print("Seeing integer's immutability")
a = 2
print(id(a))
b = a # points to a's id
print(id(b))
a = 3 # a id changes
print(id(a))
print(a,b)
b=4
print(id(b),b)

print("\n\nSeeing lists mutability")
a=[1,2,3]
print(id(a))
b = a # points to a's id BOTH SHARE THE SAME OBJECT - NOT the right way to copy
c = a.copy()
print(id(b))
print(id(c))
a.append([4,5,6])
print(id(a))
print(a)
print(b) ## B is same as A !!!
b=[7,8,9] ### b's id changes,the old one is forgotten
print(b)
print(c)




