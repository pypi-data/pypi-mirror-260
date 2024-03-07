"""
map_funcs：map 多个函数
"""
from typing import Callable, Iterable


def map_funcs(funcs: list[Callable], iterable: Iterable) -> Iterable:
    """
    map 多个函数
    """
    for func in funcs:
        iterable = map(func, iterable)
    return iterable


if __name__ == '__main__':
    a = map_funcs([lambda x: x + 1, lambda x: x + 2], [1, 2, 3])
    for i in a:
        print(i)