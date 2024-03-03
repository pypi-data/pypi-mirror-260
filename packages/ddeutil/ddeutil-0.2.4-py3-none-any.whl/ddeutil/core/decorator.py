import contextlib
import copy
from functools import wraps
from time import sleep, time


def deepcopy(func):
    """Deep copy method

    EExamples:
        >>> @deepcopy
        ... def foo(a, b, c=None):
        ...     c = c or {}
        ...     a[1] = 3
        ...     b[2] = 4
        ...     c[3] = 5
        ...     return a, b, c
        >>> aa = {1: 2}
        >>> bb = {2: 3}
        >>> cc = {3: 4}
        >>> foo(aa, bb, cc)
        ({1: 3}, {2: 4}, {3: 5})

        >>> (aa, bb, cc)
        ({1: 2}, {2: 3}, {3: 4})

    """

    def func_get(*args, **kwargs):
        return func(
            *(copy.deepcopy(x) for x in args),
            **{k: copy.deepcopy(v) for k, v in kwargs.items()},
        )

    return func_get


def deepcopy_args(func):
    """Deep copy method

    Examples:
        >>> class Foo:
        ...
        ...     @deepcopy_args
        ...     def foo(self, a, b=None):
        ...         b = b or {}
        ...         a[1] = 4
        ...         b[2] = 5
        ...         return a, b
        >>>
        >>> aa = {1: 2}
        >>> bb = {2: 3}
        >>> Foo().foo(aa, bb)
        ({1: 4}, {2: 5})

        >>> (aa, bb)
        ({1: 2}, {2: 3})

    """

    def func_get(self, *args, **kwargs):
        return func(
            self,
            *(copy.deepcopy(x) for x in args),
            **{k: copy.deepcopy(v) for k, v in kwargs.items()},
        )

    return func_get


class classproperty:
    """Decorator that converts a method with a single cls argument
    into a property that can be accessed directly from the class.

    Examples:

        >>> class Car:
        ...     wheel: int = 4
        ...     @classproperty
        ...     def foo(cls):
        ...         return "Foo" + str(cls.wheel)
        >>> Car.foo
        'Foo4'
    """

    def __init__(self, cls=None):
        self.fget = cls

    def __get__(self, instance, cls=None):
        return self.fget(cls)

    def getter(self, method):
        self.fget = method
        return self


class ClassPropertyDescriptor:
    def __init__(self, fget, fset=None):
        self.fget = fget
        self.fset = fset

    def __get__(self, obj, klass=None):
        if klass is None:
            klass = type(obj)
        return self.fget.__get__(obj, klass)()

    def __set__(self, obj, value):
        if not self.fset:
            raise AttributeError("can't set attribute")
        type_ = type(obj)
        return self.fset.__get__(obj, type_)(value)

    def setter(self, func):
        if not isinstance(func, (classmethod, staticmethod)):
            func = classmethod(func)
        self.fset = func
        return self


def class_property(func):
    """
    Examples:
        >>> class Car:
        ...     wheel: int = 4
        ...     @class_property
        ...     def foo(cls):
        ...         return "Foo" + str(cls.wheel)
        >>> Car.foo
        'Foo4'
    """
    if not isinstance(func, (classmethod, staticmethod)):
        func = classmethod(func)
    return ClassPropertyDescriptor(func)


def timer(func):
    """
    Examples:
        >>> import time
        >>> @timer
        ... def will_sleep():
        ...     time.sleep(2)
        ...     return
        >>> will_sleep()
        Execution time: 2.003119945526123 seconds
    """

    def wrapper(*args, **kwargs):
        # start the timer
        start_time = time()
        # call the decorated function
        result = func(*args, **kwargs)
        # remeasure the time
        end_time = time()
        # compute the elapsed time and print it
        execution_time = end_time - start_time
        print(f"Execution time: {execution_time} seconds")
        # return the result of the decorated function execution
        return result

    # return reference to the wrapper function
    return wrapper


def timing(name: str):
    """
    Examples:
        >>> import time
        >>> @timing("Sleep")
        ... def will_sleep():
        ...     time.sleep(2)
        ...     return
        >>> will_sleep()
        Sleep ....................................................... 2.01s
    """

    def timing_internal(func):
        @wraps(func)
        def wrap(*args, **kw):
            ts = time()
            result = func(*args, **kw)
            te = time()
            padded_name = f"{name} ".ljust(60, ".")
            padded_time = f" {(te - ts):0.2f}".rjust(6, ".")
            print(f"{padded_name}{padded_time}s", flush=True)
            return result

        return wrap

    return timing_internal


@contextlib.contextmanager
def timer_perf(title: str):
    """
    Examples:
        >>> import time
        >>> with timer_perf('Sleep'):
        ...     time.sleep(2)
        Sleep ....................................................... 2.00s
    """
    ts = time()
    yield
    te = time()
    padded_name = f"{title} ".ljust(60, ".")
    padded_time = f" {(te - ts):0.2f}".rjust(6, ".")
    print(f"{padded_name}{padded_time}s", flush=True)


def debug(func):
    """
    Examples:
        >>> @debug
        ... def add_numbers(x, y):
        ...     return x + y
        >>> add_numbers(7, y=5,)
        Calling add_numbers with args: (7,) kwargs: {'y': 5}
        add_numbers returned: 12
        12
    """

    def wrapper(*args, **kwargs):
        # print the function name and arguments
        print(f"Calling {func.__name__} with args: {args} kwargs: {kwargs}")
        # call the function
        result = func(*args, **kwargs)
        # print the results
        print(f"{func.__name__} returned: {result}")
        return result

    return wrapper


def exception_handler(func):
    """
    Examples:
        >>> @exception_handler
        ... def divide(x, y):
        ...     result = x / y
        ...     return result
        >>> divide(10, 0)
        An exception occurred: division by zero
    """

    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as err:
            # Handle the exception
            print(f"An exception occurred: {str(err)}")
            # Optionally, perform additional error handling or logging
            # Reraise the exception if needed

    return wrapper


def validate_input(*validations):
    """
    :usage:
        >>> @validate_input(lambda x: x > 0, lambda y: isinstance(y, str))
        ... def divide_and_print(x, message):
        ...     print(message)
        ...     return 1 / x
        >>> divide_and_print(5, "Hello!")
        Hello!
        0.2
    """

    def decorator(func):
        def wrapper(*args, **kwargs):
            for i, val in enumerate(args):
                if i < len(validations) and not validations[i](val):
                    raise ValueError(f"Invalid argument: {val}")
            for key, val in kwargs.items():
                if key in validations[len(args) :] and not validations[
                    len(args) :
                ][key](val):
                    raise ValueError(f"Invalid argument: {key}={val}")
            return func(*args, **kwargs)

        return wrapper

    return decorator


def retry(max_attempts, delay: int = 1):
    """
    :usage:
        >>> @retry(max_attempts=3, delay=2)
        ... def fetch_data(url):
        ...     print("Fetching the data ...")
        ...     raise TimeoutError("Server is not responding.")
        >>> fetch_data("https://example.com/data")
        Fetching the data ...
        Attempt 1 failed: Server is not responding.
        Fetching the data ...
        Attempt 2 failed: Server is not responding.
        Fetching the data ...
        Attempt 3 failed: Server is not responding.
        Function failed after 3 attempts
    """

    def decorator(func):
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempts += 1
                    print(f"Attempt {attempts} failed: {e}")
                    sleep(delay)
            print(f"Function failed after {max_attempts} attempts")

        return wrapper

    return decorator
