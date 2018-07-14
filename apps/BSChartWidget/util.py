import time


def perf_timer(argument, debug=True, limit=10):
    def real_decorator(fn):
        def wrapper(*args, **kwargs):
            if debug:
                s = time.perf_counter()
                result = fn(*args, **kwargs)
                ms = (time.perf_counter() - s) * 1000
                if ms > limit: # 100 > 10
                    print("T : {} - {:.6f} ms".format(argument, ms))
            else:
                result = fn(*args, **kwargs)

            return result
        return wrapper
    return real_decorator
