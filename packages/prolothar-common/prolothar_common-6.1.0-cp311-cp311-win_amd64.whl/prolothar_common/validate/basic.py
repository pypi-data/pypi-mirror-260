"""
constains basic identity checks
"""

def is_instance(x: any, expected_type, ex=ValueError, msg: str = None):
    """
    validates that is_instance(x, expected_type) is true

    Parameters
    ----------
    x : any
        any object whose type needs to be validated
    expected_type : any
        type argument of is_instance
    ex : _type_, optional
        constructor/callable for exception creation, by default ValueError
    msg : str, optional
        can be set to control the message of the raised exception,
        by default None, i.e. a message will be generated
    """
    if not isinstance(x, expected_type):
        if msg is None:
            msg = f'x = {x} was expected to be of type {expected_type} but was {type(x)}'
        raise ex(msg)

def is_true(x: bool, ex=ValueError, msg: str = None):
    """
    validates that x evaluates to True

    Parameters
    ----------
    x : bool
        must be True
    ex : _type_, optional
        constructor/callable for exception creation, by default ValueError
    msg : str, optional
        can be set to control the message of the raised exception,
        by default None, i.e. a message will be generated
    """
    if not x:
        if msg is None:
            msg = 'argument expected to be True but was False'
        raise ex(msg)


def equals(x, y, ex=ValueError, msg: str = None):
    """
    validates that x == y

    Parameters
    ----------
    x : any
    y : any
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
    if x != y:
        if msg is None:
            msg = f'{x} != {y}'
        raise ex(msg)

def not_equals(x, y, ex=ValueError, msg: str = None):
    """
    validates that x != y

    Parameters
    ----------
    x : any
    y : any
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
    if x == y:
        if msg is None:
            msg = f'{x} == {y}'
        raise ex(msg)

def is_not_none(x, ex=ValueError, msg: str = None):
    """
    validates that x is not None

    Parameters
    ----------
    x : any
        if None, raises ex
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
    if x is None:
        if msg is None:
            msg = 'unexpected None'
        raise ex(msg)

def less(x, y, ex=ValueError, msg: str = None):
    """
    validates that x < y

    Parameters
    ----------
    x : any
        must be comparable
    y : any
        must be comparable
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
    if x >= y:
        if msg is None:
            msg = f'{x} >= {y}'
        raise ex(msg)

def less_or_equal(x, y, ex=ValueError, msg: str = None):
    """
    validates that x <= y

    Parameters
    ----------
    x : any
        must be comparable
    y : any
        must be comparable
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
    if x > y:
        if msg is None:
            msg = f'{x} > {y}'
        raise ex(msg)

def greater(x, y, ex=ValueError, msg: str = None):
    """
    validates that x > y

    Parameters
    ----------
    x : any
        must be comparable
    y : any
        must be comparable
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
    if x <= y:
        if msg is None:
            msg = f'{x} <= {y}'
        raise ex(msg)

def greater_or_equal(x, y, ex=ValueError, msg: str = None):
    """
    validates that x >= y

    Parameters
    ----------
    x : any
        must be comparable
    y : any
        must be comparable
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
    if x < y:
        if msg is None:
            msg = f'{x} < {y}'
        raise ex(msg)

def is_in(x, y, ex=ValueError, msg: str = None):
    """
    validates that "x in y" evaluates to True

    Parameters
    ----------
    x : any
        if y uses hash keys, x must be hashable
    y : any
        must implement the "in" operator
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
    if x not in y:
        if msg is None:
            msg = f'{x} not in {y}'
        raise ex(msg)

def in_closed_interval(x, a, b, ex=ValueError, msg: str = None):
    """
    validates that a <= x <= b

    Parameters
    ----------
    x : any
        must be comparable
    a : any
        must be comparable
    b : any
        must be comparable
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
    if not (a <= x <= b):
        if msg is None:
            msg = f'failed assumption: {a} <= {x} <= {b}'
        raise ex(msg)

def in_open_interval(x, a, b, ex=ValueError, msg: str = None):
    """
    validates that a < x < b

    Parameters
    ----------
    x : any
        must be comparable
    a : any
        must be comparable
    b : any
        must be comparable
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
    if not (a < x < b):
        if msg is None:
            msg = f'failed assumption: {a} < {x} < {b}'
        raise ex(msg)

def in_left_open_interval(x, a, b, ex=ValueError, msg: str = None):
    """
    validates that a < x <= b

    Parameters
    ----------
    x : any
        must be comparable
    a : any
        must be comparable
    b : any
        must be comparable
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
    if not (a < x <= b):
        if msg is None:
            msg = f'failed assumption: {a} < {x} <= {b}'
        raise ex(msg)

def in_right_open_interval(x, a, b, ex=ValueError, msg: str = None):
    """
    validates that a <= x < b

    Parameters
    ----------
    x : any
        must be comparable
    a : any
        must be comparable
    b : any
        must be comparable
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
    if not (a <= x < b):
        if msg is None:
            msg = f'failed assumption: {a} <= {x} < {b}'
        raise ex(msg)
