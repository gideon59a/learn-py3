def pfib(*args, **kwargs):
    print(args) ## prints the tupple (1,1)
    print(kwargs) ## prints the dict {'th': 2}

def wrapper(*args, **kwargs):
    print(*args)  ## adding the star unpacks the tupple so we get 1,1 instead of (1,1)
    # print(**kwargs) ## printing it would fail, as print can't handle the th.
    print('Leaving wrapper')
    pfib(*args, **kwargs)

print(pfib())
print(wrapper(1, 1, th=2))