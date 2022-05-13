import time


def perftimer(func):
    """
    A timer decorator to time to runtime of a function
    add @perftimer above a function to make use of it.
    output is string in seconds
    """
    def wrapper(*args, **kwargs):
        start = time.time()
        outcome = func(*args, **kwargs)
        stop = time.time() - start
        print(f"--- Process {func.__name__} ran in: {stop:.5f}s ---")
        return outcome
    return wrapper
