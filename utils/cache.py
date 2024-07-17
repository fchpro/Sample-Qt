from logger_config import log_args_kwargs as print
from functools import wraps

# Cache which uses a key kwarg for uniqueness. Allows us to cache, even when
# we have unhashable types on the parameters (e.g. dicts).


def key_cache(fn):
    """Decorator that will cache calls to a function, using a key."""
    _cache = {}

    @wraps(fn)
    def wrapper(*args, **kwargs):
        cache_key = f"{args}/{kwargs}"
        if cache_key in _cache:
            return _cache[cache_key]

        _cache[cache_key] = fn(*args, **kwargs)
        return _cache[cache_key]

    return wrapper


# Cache which uses a key kwarg for uniqueness. Allows us to cache, even when
# we have unhashable types on the parameters (e.g. dicts).


def key_cache(fn):
    """Decorator that will cache calls to a function, using a key."""
    _cache = {}

    @wraps(fn)
    def wrapper(*args, **kwargs):
        cache_key = f"{args}/{kwargs}"
        if cache_key in _cache:
            return _cache[cache_key]

        _cache[cache_key] = fn(*args, **kwargs)
        return _cache[cache_key]

    return wrapper
