class ValueCheckError(ValueError):
    def __init__(self, message: str = ""):
        super().__init__(message)

class TypeCheckError(TypeError):
    def __init__(self, message: str = "") -> None:
        super().__init__(message)

class WrongLiteral(ValueCheckError):
    def __init__(self, arg_name: str = None, arg_value=None, allowed_values: list | tuple = None):
        if arg_name is None or allowed_values is None:
            super().__init__()
        else:
            msg = f"Argument '{arg_name}' ({arg_value}) must match one of the following values: {', '.join(allowed_values)}"
            super().__init__(msg)

class WrongType(TypeCheckError):
    """
    Raised when type does not match expected type.
    """
    def __init__(self, arg_name: str = None, arg_value: str = None, expected_type = None):
        if arg_name is None or arg_value is None:
            super().__init__()
        else:
            msg = f"Expected argument '{arg_name}' ({arg_value}) to be an instance of {expected_type.__name__}, got {type(arg_value).__name__} instead"
            super().__init__(msg)

class WrongTypes(TypeCheckError):
    """
    Raised when type does not match any of the types in a union.
    """
    def __init__(self, arg_name: str = None, arg_value: str = None):
        if arg_name is None or arg_value is None:
            super().__init__()
        else:
            msg = f"Argument '{arg_name}' ({arg_value}) of type {type(arg_value).__name__} does not match any of the allowed types"
            super().__init__(msg)

class WrongItem(TypeCheckError):
    """
    Raised when the items in a list-like value do not all match the expected types.
    """
    def __init__(self, arg_name: str = None, idx: int = None):
        if arg_name is None or idx is None:
            super().__init__()
        else:
            msg = f"Item {idx} of {arg_name}"
            super().__init__(msg)

class NotListLike(TypeCheckError):
    """
    Raised when value is not of a list-like type.
    """
    def __init__(self, arg_name: str = None, arg_value: str = None) -> None:
        if arg_name is None or arg_value is None:
            super().__init__()
        else:
            msg = f"Argument '{arg_name}' ({arg_value}) must be a collection of some kind, got {type(arg_value).__name__} instead"
            super().__init__(msg)

