#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# File          : __init__.py
# Author        : Sun YiFan-Movoid
# Time          : 2024/3/2 20:58
# Description   : 
"""
from __future__ import annotations

import inspect
import typing
from abc import ABC
from typing import Union, Any


def get(element: type | None) -> str:
    """
    Returns the element name with the relative module and adds the module to the imports (if it is not yet present)
    :param element: the element
    :return:
    :rtype: str
    """
    # The element can be a string, for example "def f() -> 'SameClass':..."
    if isinstance(element, str):
        print('str')
        return element
    elif isinstance(element, type):
        print('type')
        module = inspect.getmodule(element)
        if module is None or module.__name__ == 'builtins' or module.__name__ == '__main__':
            return element.__name__

        module_name = module.__name__

        return '{0}.{1}'.format(module_name, element.__name__)
    elif inspect.getmodule(element) == inspect.getmodule(typing):
        print('typing')
        module_name = str(element).split('.')[0]

        return str(element)


# print(get(None))
a = 1
print(inspect.ismodule(a))


# print(get.__annotations__)
# print(inspect.getmodule(get))
# print(inspect.getmodule(Union))
# print(get(get.__annotations__['element']))

class A:
    pass


class B(metaclass=A):
    pass


class C(A):
    pass


class D(B, C):
    pass


print(D.__bases__, D.__class__)

if __name__ == '__main__':
    pass
