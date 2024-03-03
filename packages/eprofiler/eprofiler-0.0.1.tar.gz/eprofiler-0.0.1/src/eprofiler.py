from datetime import datetime


def timeit(stats=None):
    """simple decorator to track duration of a function

    :param stats: optional if given can be used as a dict otherwise duration printed
    :return: dict stats
    """
    def wrapper(f):
        def inner(*args, **kwargs):
            start_time = datetime.now()
            res = f(*args, **kwargs)  # Allow for function arguments
            end_time = datetime.now()
            if stats is not None:
                stats['start_time'] = start_time
                stats['end_time'] = end_time
                stats['duration'] = end_time - start_time
            else:
                print(end_time - start_time)
            return res
        return inner
    return wrapper
