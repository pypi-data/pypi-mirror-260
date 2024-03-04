"""
contains collection (e.g. lists or set) specific validations
"""

from typing import Collection

def not_empty(x: Collection, ex=ValueError, msg: str = None):
    """
    validates that x is not empty

    Parameters
    ----------
    x : Collection
    ex : _type_, optional
        constructor/callable for exception creation, by default ValueError
    msg : str, optional
        can be set to control the message of the raised exception,
        by default None, i.e. a message will be generated

    Raises
    ------
    ex
        by default this is a ValueError
    """
    if not x:
        if msg is None:
            msg = 'the collection is not allowed to be empty'
        raise ex(msg)

def is_subset(x: Collection, y: Collection, ex=ValueError, msg: str = None):
    """
    validates that x is a subset of y

    Parameters
    ----------
    x : Collection
    y : Collection
    ex : _type_, optional
        constructor/callable for exception creation, by default ValueError
    msg : str, optional
        can be set to control the message of the raised exception,
        by default None, i.e. a message will be generated

    Raises
    ------
    ex
        by default this is a ValueError
    """
    if not set(x).issubset(y):
        if msg is None:
            msg = f'{x} is no subset of {y}'
        raise ex(msg)

def same_size(x: Collection, y: Collection, ex=ValueError, msg: str = None):
    """
    validates that len(x) == len(y)

    Parameters
    ----------
    x : Collection
    y : Collection
    ex : _type_, optional
        constructor/callable for exception creation, by default ValueError
    msg : str, optional
        can be set to control the message of the raised exception,
        by default None, i.e. a message will be generated

    Raises
    ------
    ex
        by default this is a ValueError
    """
    if len(x) != len(y):
        if msg is None:
            msg = f'len({x}) != len({y})'
        raise ex(msg)

def same_size_or_larger(x: Collection, y: Collection, ex=ValueError, msg: str = None):
    """
    validates that len(x) >= len(y)

    Parameters
    ----------
    x : Collection
    y : Collection
    ex : _type_, optional
        constructor/callable for exception creation, by default ValueError
    msg : str, optional
        can be set to control the message of the raised exception,
        by default None, i.e. a message will be generated

    Raises
    ------
    ex
        by default this is a ValueError
    """
    if len(x) < len(y):
        if msg is None:
            msg = f'len({x}) < len({y})'
        raise ex(msg)

def larger(x: Collection, y: Collection, ex=ValueError, msg: str = None):
    """
    validates that len(x) > len(y)

    Parameters
    ----------
    x : Collection
    y : Collection
    ex : _type_, optional
        constructor/callable for exception creation, by default ValueError
    msg : str, optional
        can be set to control the message of the raised exception,
        by default None, i.e. a message will be generated

    Raises
    ------
    ex
        by default this is a ValueError
    """
    if len(x) <= len(y):
        if msg is None:
            msg = f'len({x}) <= len({y}) but should be greater'
        raise ex(msg)