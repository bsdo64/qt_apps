import time


def perf_timer(argument, debug=True):
    def real_decorator(fn):
        def wrapper(*args, **kwargs):
            if debug:
                s = time.perf_counter()
                result = fn(*args, **kwargs)
                print("T : {} - {:.6f} ms".format(argument, (time.perf_counter() - s) * 1000))
            else:
                result = fn(*args, **kwargs)

            return result
        return wrapper
    return real_decorator
