"""
Contains generic helper funcitons to aid in parsing.
"""

import itertools


def take_while(predicate, items):
    return list(itertools.takewhile(predicate, items))


def drop_while(predicate, items):
    return list(itertools.dropwhile(predicate, items))


def not_(func):
    return lambda *args, **kwargs: not func(*args, **kwargs)


def first(predicate, iterable):
    for item in iterable:
        if predicate(item):
            return item
    return None


def rfirst(predicate, iterable):
    return first(predicate, reversed(list(iterable)))


def quote(string, char='"'):
    return char + string + char


def catch(func, *args, **kwargs):
    """
    Executes `func` with `args` and `kwargs` as arguments. If `func` throws an error, this function
    returns the error, otherwise it returns `None`.
    """
    try:
        func(*args, **kwargs)
    except Exception as error:
        return error
