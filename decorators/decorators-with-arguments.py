# from https://realpython.com/primer-on-python-decorators/#decorators-with-arguments
import functools
import time


def repeat(num_times):
    def decorator_repeat(func):
        @functools.wraps(func)
        def wrapper_repeat(*args, **kwargs):
            wrapper_repeat.num_calls += 1  # Stateful !!
            start_time = time.perf_counter()  # 1 Open timer
            print(f"Call {wrapper_repeat.num_calls} of {func.__name__!r}")  # see func name

            for _ in range(num_times):
                value = func(*args, **kwargs)  # This line print the "Hello <name>"
                print("value calculated")

            end_time = time.perf_counter()  # 2 Timer
            run_time = end_time - start_time  # 3 Timer
            print(f"Finished {func.__name__!r} in {run_time:.8f} secs")  # timer

            return value  # This return the wrapped function value. I could replace it with whatever.

        wrapper_repeat.num_calls = 0  # Init the stateful argument
        return wrapper_repeat
    return decorator_repeat


@repeat(num_times=3)
def greet(name):
    '''Greeting function'''
    print(f"Hello {name}")
    return 42


print(help(greet))  # W/o the functools, we see the greet function = wrapper_repeat
print(greet("Alice"))
print(greet("Emma"))
