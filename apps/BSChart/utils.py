from colorama import init, Fore
import pprint
import time


init(autoreset=True)


def perf_timer(argument, debug=True, limit=5):
    def real_decorator(fn):
        def wrapper(*args, **kwargs):
            if debug:
                s = time.perf_counter()
                result = fn(*args, **kwargs)
                ms = (time.perf_counter() - s) * 1000
                if ms > limit:  # 100 > 10
                    s = "T : {} - {:.6f} ms ".format(argument, ms)

                    if 0 <= ms < 10:
                        print(Fore.BLUE + s + '(high)')
                    elif 10 <= ms < 100:
                        print(Fore.GREEN + s + '(middle)')
                    else:
                        print(Fore.RED + s + '(low)')

            else:
                result = fn(*args, **kwargs)

            return result
        return wrapper
    return real_decorator


def attach_timer(cls, limit=5):
    parent = cls.mro()[1]
    diff_method = set(dir(cls)) - set(dir(parent))
    method_list = [
        (getattr(cls, func), func) for func in dir(cls) if
        callable(getattr(cls, func)) and
        not func.startswith("__") and
        (func in diff_method or
        (hasattr(parent, func) and getattr(parent, func) != getattr(cls, func)))
    ]

    # pprint.pprint(method_list)

    for f, n in method_list:
        setattr(cls, n, perf_timer(cls.__name__ + '.' + n, limit=limit)(f))
