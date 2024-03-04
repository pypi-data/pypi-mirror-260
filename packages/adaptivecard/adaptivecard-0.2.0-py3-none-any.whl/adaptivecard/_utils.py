from typing import get_origin, get_args, Union, Literal, Any, _GenericAlias
from types import NoneType, UnionType, GenericAlias
from adaptivecard._typing import ListLike
from adaptivecard.exceptions import TypeCheckError, ValueCheckError, WrongLiteral, WrongType, WrongTypes, WrongItem, NotListLike
from json import dump


def raise_invalid_pixel_error(arg_name: str, arg_value: str):
    msg = f"argument '{arg_name}' must be numeric or a number ending with 'px', got '{arg_value}' instead"
    raise ValueError(msg)


def convert_to_pixel_string(s):
    if isinstance(s, str):
        if not s.replace('px', '').isdecimal():
            raise ValueError
        s = s.replace('px', '') + 'px'
    elif isinstance(s, int):
        s = str(s) + 'px'
    return s

def is_union(tp):
    """
    Checks if tp is a Union. For unsubscripted Unions, will return False.
    """
    if (origin := get_origin(tp)) is Union or origin is UnionType:
        return True
    return False

def is_type(tp):
    """
    Checks if tp is a type in a broad sense. Anything that can be used as a type hint will be
    considered a type, except Unions and Literal.
    """
    return (isinstance(tp, (type, GenericAlias, _GenericAlias)) and not isinstance(tp, UnionType)) \
    and get_origin(tp) is not Literal

def is_parameterized_type(tp):
    """
    Checks if type is a GenericAlias.
    """
    return isinstance(tp, (GenericAlias, _GenericAlias))

def check_type(arg_name: str | None, arg_value: Any, expected_type):
    """
    Type-checking function, raises TypeError if arg_value doesn't match the expected type.
    """
    if expected_type is Any:
        return

    if is_union(expected_type):
        expected_type = get_args(expected_type)

    if get_origin(expected_type) is Literal:
        if arg_value not in (allowed_values := get_args(expected_type)):
            raise WrongLiteral(arg_name, arg_value, allowed_values)
        return

    elif isinstance(expected_type, tuple):
        for sub_type in expected_type:
            try:
                return check_type(arg_name, arg_value, sub_type)
            except (TypeCheckError, ValueCheckError):
                continue
        else:
            raise WrongTypes(arg_name, arg_value)
    elif is_type(expected_type):
        if is_parameterized_type(expected_type):
            type_origin = get_origin(expected_type)
            type_subscripts = get_args(expected_type)
            check_type(arg_name, arg_value, type_origin)
            container = arg_value
            if type_origin is tuple:
                ... # devo tratar tuplas? Se sim, como?
            else:
                for i, item in enumerate(container):
                    try:
                        check_type(arg_name, item, type_subscripts)
                    except (TypeCheckError, ValueCheckError):
                        raise WrongItem(arg_name, i)
                return
        else:
            if (expected_type is NoneType and arg_value is not None) or \
                (not isinstance(arg_value, expected_type)):
                if expected_type is ListLike:
                    raise NotListLike(arg_name, arg_value)
                raise WrongType(arg_name, arg_value, expected_type)
            return
    else:
        raise Exception("Invalid!")  

def camel_to_snake(s: str):
    l = list(s)
    for i, char in enumerate(l):
        if (lower_char := char.lower()) != char:
            l[i] = "_" + lower_char if i > 0 else lower_char
    return "".join(l)

def snake_to_camel(s: str):
    l = s.split("_")
    for i, word in enumerate(l):
        if i > 0:
            l[i] = word.capitalize()
    return "".join(l)

def save_json(path: str, obj: dict, indent: int = 4):
    if not isinstance(indent, int):
        raise TypeError
    with open(path, 'w') as f:
        dump(obj, f, indent=indent)
