import functools
import warnings


def deprecated_params(param_mapping):
    def decorator_init(func):
        @functools.wraps(func)
        def wrapper_init(*args, **kwargs):
            for old_param, new_param in param_mapping.items():
                if old_param in kwargs:
                    warnings.warn(f"Parameter '{old_param}' is deprecated. Use '{new_param}' instead.",
                                  category=DeprecationWarning, stacklevel=2)
                    kwargs[new_param] = kwargs.pop(old_param)
            return func(*args, **kwargs)
        return wrapper_init
    return decorator_init

