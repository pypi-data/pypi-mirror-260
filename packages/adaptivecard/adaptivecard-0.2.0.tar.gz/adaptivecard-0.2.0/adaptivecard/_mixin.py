from typing import Any, get_type_hints
from adaptivecard._typing import DefaultNone
from adaptivecard._utils import check_type, snake_to_camel


class Mixin:
    __slots__ = ()

    def to_dict(self):
        dic = {}
        for attr_name, attr_value in {attr_name: getattr(self, attr_name) for attr_name in self.__slots__ if hasattr(self, attr_name)}.items():
            camel_formated_attr_name = snake_to_camel(attr_name)
            if hasattr(attr_value, "__slots__"):
                dic[camel_formated_attr_name] = attr_value.to_dict()
            elif isinstance(attr_value, list):
                dic[camel_formated_attr_name] = [inner_value.to_dict() for inner_value in attr_value if hasattr(inner_value, "__slots__")]
            else:
                attr_value = attr_value if attr_value is not None else "none"
                dic[camel_formated_attr_name] = attr_value
        return dic

    def __setattr__(self, __name: str, __value: Any) -> None:
        # do not create attributes that are set to DefaultNone, i.e., the user did not input any value
        if __value is DefaultNone:
            return
        type_hints = get_type_hints(self.__init__)
        check_type(__name, __value, type_hints.get(__name, Any))
        super().__setattr__(__name, __value)
