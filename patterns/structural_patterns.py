from time import time

routes = dict()


class AppRoute:
    """Decorator"""

    def __init__(self, url):
        self.routes = routes
        self.url = url

    def __call__(self, cls):
        self.routes[self.url] = cls()


class Debug:
    """Decorator"""

    def __init__(self, name):
        self.name = name

    def __call__(self, cls):
        def timeit(method):
            def timed(*args, **kw):
                ts = time()
                result = method(*args, **kw)
                te = time()
                delta = te - ts

                print(f'DEBUG: {self.name} took {delta:2.2f} ms')
                return result

            return timed

        return timeit(cls)
