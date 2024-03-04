from typing import Any, Literal
import adaptivecard._base_types as _base_types
from adaptivecard._typing import ListLike, DefaultNone, ChoiceList
from adaptivecard._mixin import Mixin


class Text(Mixin):
    __slots__ = ("type", "id", "is_multiline", "max_length", "placeholder",
                 "regex", "style", "inline_action", "value", "wrap", "error_message",
                 "is_required", "label", "fallback", "height", "separator", "spacing", "is_visible")

    def __init__(self,
                 id: str,
                 is_multiline: bool = DefaultNone,
                 max_length: int = DefaultNone,
                 placeholder : str = DefaultNone,
                 regex: str = DefaultNone,
                 style: str = DefaultNone,
                 inline_action : _base_types.Action = DefaultNone,
                 value: str = DefaultNone,
                 error_message: str = DefaultNone,
                 is_required : bool = DefaultNone,
                 label: str = DefaultNone,
                 fallback: _base_types.Element = DefaultNone,
                 height: Literal["auto", "stretch"] = DefaultNone,
                 separator: bool = DefaultNone,
                 spacing: Literal["default", "none", "small", "medium", "large", "extraLarge",
                                  "padding"] | None = DefaultNone,
                 is_visible: bool = DefaultNone,
                 ):
        self.type = "Input.Text"
        self.id = id
        self.is_multiline = is_multiline
        self.max_length = max_length
        self.placeholder = placeholder
        self.regex = regex
        self.style = style
        self.inline_action = inline_action
        self.value = value
        self.error_message = error_message
        self.is_required = is_required
        self.label = label
        self.fallback = fallback
        self.height = height
        self.separator = separator
        self.spacing = spacing
        self.is_visible = is_visible


class Number(Mixin):
    __slots__ = ("type", "id", "max", "min", "placeholder",
                 "value", "wrap", "error_message", "is_required", "label", "fallback",
                 "height", "separator", "spacing", "is_visible")

    def __init__(self,
                 id: str,
                 max: int = DefaultNone,
                 min: int = DefaultNone,
                 placeholder: str = DefaultNone,
                 value: int = DefaultNone,
                 error_message: str = DefaultNone,
                 is_required : bool = DefaultNone,
                 label: str = DefaultNone,
                 fallback: _base_types.Element = DefaultNone,
                 height: Literal["auto", "stretch"] = DefaultNone,
                 separator: bool = DefaultNone,
                 spacing: Literal["default", "none", "small", "medium", "large", "extraLarge",
                                  "padding"] | None = DefaultNone,
                 is_visible: bool = DefaultNone,
                 ):

        self.type = "Input.Number"
        self.id = id
        self.max = max
        self.min = min
        self.placeholder = placeholder
        self.value = value
        self.error_message = error_message
        self.is_required = is_required
        self.label = label
        self.fallback = fallback
        self.height = height
        self.separator = separator
        self.spacing = spacing
        self.is_visible = is_visible


class Date(Mixin):
    __slots__ = ("type", "id", "max", "min", "placeholder", "value", "error_message", "is_required",
                 "label", "fallback", "height", "separator", "spacing", "is_visible")
    def __init__(self,
                 id: str,
                 max: str = DefaultNone,
                 min: str = DefaultNone,
                 placeholder: str = DefaultNone,
                 value: str = DefaultNone,
                 error_message: str = DefaultNone,
                 is_required : bool = DefaultNone,
                 label: str = DefaultNone,
                 fallback: _base_types.Element = DefaultNone,
                 height: Literal["auto", "stretch"] = DefaultNone,
                 separator: bool = DefaultNone,
                 spacing: Literal["default", "none", "small", "medium", "large", "extraLarge",
                                  "padding"] | None = DefaultNone,
                 is_visible: bool = DefaultNone,) -> None:

        self.type = "Input.Date"
        self.id = id
        self.max = max
        self.min = min
        self.placeholder = placeholder
        self.value = value
        self.error_message = error_message
        self.is_required = is_required
        self.label = label
        self.fallback = fallback
        self.height = height
        self.separator = separator
        self.spacing = spacing
        self.is_visible = is_visible


class Time(Mixin):
    __slots__ = ("type", "id", "max", "min", "placeholder", "value", "error_message", "is_required",
                 "label", "fallback", "height", "separator", "spacing", "is_visible")
    def __init__(self,
                 id: str,
                 max: str = DefaultNone,
                 min: str = DefaultNone,
                 placeholder: str = DefaultNone,
                 value: str = DefaultNone,
                 error_message: str = DefaultNone,
                 is_required : bool = DefaultNone,
                 label: str = DefaultNone,
                 fallback: _base_types.Element = DefaultNone,
                 height: Literal["auto", "stretch"] = DefaultNone,
                 separator: bool = DefaultNone,
                 spacing: Literal["default", "none", "small", "medium", "large", "extraLarge",
                                  "padding"] | None = DefaultNone,
                 is_visible: bool = DefaultNone):

        self.type = "Input.Time"
        self.id = id
        self.max = max
        self.min = min
        self.placeholder = placeholder
        self.value = value
        self.error_message = error_message
        self.is_required = is_required
        self.label = label
        self.fallback = fallback
        self.height = height
        self.separator = separator
        self.spacing = spacing
        self.is_visible = is_visible        


class DataQuery(Mixin):
    __slots__ = ("type", "dataset", "count", "skip")
    def __init__(self,
                 dataset: str,
                 count: int = DefaultNone,
                 skip: int = DefaultNone
                 ):

        self.type = "Data.Query"
        self.dataset = dataset
        self.count = count
        self.skip = skip


class Toggle(Mixin):
    __slots__ = ('type', 'title', 'id', 'value', 'value_off', 'value_on', 'wrap', 'error_message',
                 'is_required', 'label', 'fallback', 'height', 'separator', 'spacing', 'is_visible')
    def __init__(self,
                 title: str,
                 id: str,
                 value: bool = DefaultNone,
                 value_off: bool = DefaultNone,
                 value_on: bool = DefaultNone,
                 wrap: bool = DefaultNone,
                 error_message: str = DefaultNone,
                 is_required : bool = DefaultNone,
                 label: str = DefaultNone,
                 fallback: _base_types.Element = DefaultNone,
                 height: Literal["auto", "stretch"] = DefaultNone,
                 separator: bool = DefaultNone,
                 spacing: Literal["default", "none", "small", "medium", "large", "extraLarge",
                                  "padding"] | None = DefaultNone,
                 is_visible: bool = DefaultNone):

        self.type = "Input.Toggle"
        self.title = title
        self.id = id
        self.value = value
        self.value_off = value_off
        self.value_on = value_on
        self.wrap = wrap
        self.error_message = error_message
        self.is_required = is_required
        self.label = label
        self.fallback = fallback
        self.height = height
        self.separator = separator
        self.spacing = spacing
        self.is_visible = is_visible  


class Choice(Mixin):
    __slots__ = ("title", "value")
    def __init__(self,
                 title: str,
                 value: str
                 ):
        self.title = title
        self.value = value


class ChoiceSet(Mixin):
    __slots__ = ("type", "id", "choices", "choices_data", "is_multiselect", "style", "value",
                 "placeholder", "wrap", "error_message", "is_required", "label", "fallback",
                 "height", "separator", "spacing", "is_visible")
    def __init__(self,
                 id: str,
                 choices: Choice| ListLike[Choice] = DefaultNone,
                 choices_data: DataQuery = DefaultNone,
                 is_multiselect: bool = DefaultNone,
                 style: Literal["compact", "extended", "filtered"] = DefaultNone,
                 value: str = DefaultNone,
                 placeholder: str = DefaultNone,
                 wrap: bool = DefaultNone,
                 error_message: str = DefaultNone,
                 is_required : bool = DefaultNone,
                 label: str = DefaultNone,
                 fallback: _base_types.Element = DefaultNone,
                 height: Literal["auto", "stretch"] = DefaultNone,
                 separator: bool = DefaultNone,
                 spacing: Literal["default", "none", "small", "medium", "large", "extraLarge",
                                  "padding"] | None = DefaultNone,
                 is_visible: bool = DefaultNone,
                 ):

        self.type = "Input.ChoiceSet"
        self.id = id
        self.choices: ChoiceList = choices
        self.choices_data = choices_data
        self.is_multiselect = is_multiselect
        self.style = style
        self.value = value
        self.placeholder = placeholder
        self.wrap = wrap
        self.error_message = error_message
        self.is_required = is_required
        self.label = label
        self.fallback = fallback
        self.height = height
        self.separator = separator
        self.spacing = spacing
        self.is_visible = is_visible

    def to_dict(self):
        dic = {}
        for attr_name in self.__slots__:
            if hasattr(self, attr_name):
                attr_value = getattr(self, attr_name)
                if attr_value == "choices_data":
                    attr_value = attr_value.replace('_', '.')
                dic[attr_name] = attr_value
        return dic

    def __setattr__(self, __name: str, __value: Any) -> None:
        if __name == "choices":
            if isinstance(__value, Choice):
                __value = ChoiceList([__value])
            elif isinstance(__value, ListLike) and not isinstance(__value, ChoiceList):
                __value = ChoiceList(__value)
            
        return super().__setattr__(__name, __value)
    

_base_types.Text.register(Text)
_base_types.Number.register(Number)
_base_types.Date.register(Date)
_base_types.Time.register(Time)
_base_types.Toggle.register(Toggle)
_base_types.Choice.register(Choice)
_base_types.ChoiceSet.register(ChoiceSet)


