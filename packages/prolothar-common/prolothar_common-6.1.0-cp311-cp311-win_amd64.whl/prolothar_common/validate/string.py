"""
contains validation functions for strings
"""

import re

def not_empty(x: str, ex=ValueError, msg: str = None):
    """
    validates that x is not the empty string, i.e. a string with no characters

    Parameters
    ----------
    x : str
        must not be ""
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
            msg = 'the string is not allowed to be empty'
        raise ex(msg)

def startswith(x: str, prefix: str, ex=ValueError, msg: str = None):
    """
    validates that x starts with the given prefix

    Parameters
    ----------
    x : str
        a string that is supposed to start with the given prefix
    prefix : str
        x is supposed to start with this prefix
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
    if not x.startswith(prefix):
        if msg is None:
            msg = f'{x} does not start with {prefix}'
        raise ex(msg)

def endswith(x: str, suffix: str, ex=ValueError, msg: str = None):
    """
    validates that x ends with the given suffix

    Parameters
    ----------
    x : str
        a string that is supposed to start with the given prefix
    suffix : str
        x is supposed to end with this suffix
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
    if not x.endswith(suffix):
        if msg is None:
            msg = f'{x} does not end with {suffix}'
        raise ex(msg)

def matches(x: str, regex: str|re.Pattern, ex=ValueError, msg: str = None):
    """
    validates that x matches the given regular expression

    Parameters
    ----------
    x : str
        a string that is supposed to start with the given prefix
    regex : str
        a regular expression
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
    if not re.fullmatch(regex, x):
        if msg is None:
            msg = f'{x} does not match regular expression {regex}'
        raise ex(msg)
