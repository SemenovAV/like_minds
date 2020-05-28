_context = {}


class SingletonMeta(type):
    _instance = None
    def __call__(self):
        if self._instance is None:
            self._instance = super().__call__()
        return self._instance


class Context(metaclass=SingletonMeta):
    def __setattr__(self, key, value):
        if key in _context:
            return
        else:
            _context[key] = value

    def __getattr__(self, item):
        if item in _context:
            return _context[item]


    @staticmethod
    def update(**kwargs):
        _context.update(kwargs)


context = Context()


def get_context(f):
    return lambda *args, **kwargs: f(*args, **kwargs, this_app_context=context)
