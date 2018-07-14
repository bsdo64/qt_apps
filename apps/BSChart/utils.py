from colorama import init, Fore
import pprint
import time


init(autoreset=True)


def perf_timer(argument, debug=True, limit=1):
    def real_decorator(fn):
        def wrapper(*args, **kwargs):
            if debug:
                s = time.perf_counter()
                result = fn(*args, **kwargs)
                ms = (time.perf_counter() - s) * 1000
                if ms > limit:  # 100 > 10
                    s = " ->\t{} - {:.6f} ms ".format(argument, ms)

                    if 0 <= ms < 5:
                        print(Fore.BLUE + 'T1' + s)
                    elif 5 <= ms < 10:
                        print(Fore.GREEN + 'T2' + s)
                    elif 10 <= ms < 50:
                        print(Fore.YELLOW + 'T3' + s)
                    elif 50 <= ms < 100:
                        print(Fore.LIGHTRED_EX + 'T4' + s)
                    else:
                        print(Fore.RED + 'T5' + s)

            else:
                result = fn(*args, **kwargs)

            return result
        return wrapper
    return real_decorator


def attach_timer(cls, limit=0):
    parent = cls.mro()[1]
    diff_method = set(dir(cls)) - set(dir(parent))
    method_list = [
        (getattr(cls, func), func) for func in dir(cls) if
        callable(getattr(cls, func)) and
        # not func.startswith("__") and
        (func in diff_method or
        (hasattr(parent, func) and getattr(parent, func) != getattr(cls, func)))
    ]

    pprint.pprint(method_list)

    for f, n in method_list:
        setattr(cls, n, perf_timer(cls.__name__ + '.' + n, limit=limit)(f))
