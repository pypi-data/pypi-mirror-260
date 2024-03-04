from typing import Literal
from adaptivecard._mixin import Mixin
import adaptivecard._base_types as _base_types
from adaptivecard._typing import ListLike, DefaultNone


class ShowCard(Mixin):
    __slots__ = ('type', 'title', 'icon_url', 'id', 'style', 'fallback', 'tooltip', 'is_enabled',
                 'mode', 'card')
    def __init__(self,
                 card: _base_types.AdaptiveCard,
                 title: str = DefaultNone,
                 icon_url: str = DefaultNone,
                 id: str = DefaultNone,
                 style: Literal["default", "positive", "destructive"] = DefaultNone,
                 fallback: _base_types.Action = DefaultNone,
                 tooltip: str = DefaultNone,
                 is_enabled: bool = DefaultNone,
                 mode: Literal["primary", "secondary"] = DefaultNone):
        
        self.type = "Action.ShowCard"
        self.title = title
        self.icon_url = icon_url
        self.id = id
        self.style = style
        self.fallback = fallback
        self.tooltip = tooltip
        self.is_enabled = is_enabled
        self.mode = mode
        self.card = card


class OpenUrl(Mixin):
    __slots__ = ("url", "title", "id", "style", "fallback", "tooltip", "is_enabled", "mode")
    def __init__(self,
                 url: str,
                 title: str = DefaultNone,
                 id: str = DefaultNone,
                 style: Literal["default", "positive", "destructive"] = DefaultNone,
                 fallback: _base_types.Action  = DefaultNone,
                 tooltip: str = DefaultNone,
                 is_enabled: bool = DefaultNone,
                 mode: Literal["primary", "secondary"] = DefaultNone):

        self.type = "Action.OpenUrl"
        self.title = title
        self.url = url
        self.id = id
        self.style = style
        self.fallback = fallback
        self.tooltip = tooltip
        self.is_enabled = is_enabled
        self.mode = mode


class Submit(Mixin):
    __slots__ = ("type", "data", "associated_inputs", "title", "icon_url", "id", "style", "fallback",
                 "tooltip", "is_enabled", "mode")
    def __init__(self,
                 data: dict,
                 associated_inputs: Literal["auto", "none"] | None,
                 title: str = DefaultNone,
                 icon_url: str = DefaultNone,
                 id: str = DefaultNone,
                 style: Literal["default", "positive", "destructive"] = DefaultNone,
                 fallback: _base_types.Action = DefaultNone,
                 tooltip: str = DefaultNone,
                 is_enabled: bool = DefaultNone,
                 mode: Literal["primary", "secondary"] = DefaultNone):

        self.type = "Action.ToggleVisibility"
        self.data = data
        self.associated_inputs = associated_inputs
        self.title = title
        self.icon_url = icon_url
        self.id = id
        self.style = style
        self.fallback = fallback
        self.tooltip = tooltip
        self.is_enabled = is_enabled
        self.mode = mode


class TargetElement(Mixin):
    __slots__ = ("element_id", "is_visible")
    def __init__(self,
                 element_id: str,
                 is_visible: bool):
        self.element_id = element_id
        self.is_visible = is_visible


class ToggleVisibilty(Mixin):
    __slots__ = ("type", "data", "target_elements", "icon_url", "title", "id", "style", "fallback",
                 "tooltip", "is_enabled", "mode")
    def __init__(self,
                 data: str | dict,
                 target_elements: ListLike[TargetElement],
                 icon_url: str = DefaultNone,
                 title: str = DefaultNone,
                 id: str = DefaultNone,
                 style: Literal["default", "positive", "destructive"] = DefaultNone,
                 fallback: _base_types.Action = DefaultNone,
                 tooltip: str = DefaultNone,
                 is_enabled: bool = DefaultNone,
                 mode: Literal["primary", "secondary"] = DefaultNone):

        self.type = "Input.ToggleVisibility"
        self.data = data
        self.target_elements = target_elements
        self.icon_url = icon_url
        self.title = title
        self.id = id
        self.style = style
        self.fallback = fallback
        self.tooltip = tooltip
        self.is_enabled = is_enabled
        self.mode = mode

    
class Execute(Mixin):
    __slots__ = ()
    def __init__(self,
                 verb: str = DefaultNone,
                 data: dict = DefaultNone,
                 associated_inputs: Literal["auto", "none"] | None = DefaultNone,
                 title: str = DefaultNone,
                 icon_url: str = DefaultNone,
                 id: str = DefaultNone,
                 style: Literal["default", "positive", "destructive"] = DefaultNone,
                 fallback: _base_types.Action = DefaultNone,
                 tooltip: str = DefaultNone,
                 is_enabled: bool = DefaultNone,
                 mode: Literal["primary", "secondary"] = DefaultNone):
        
        self.type = "Input.Execute"
        self.verb = verb
        self.data = data
        self.associated_inputs = associated_inputs
        self.title = title
        self.icon_url = icon_url
        self.id = id
        self.style = style
        self.fallback = fallback
        self.tooltip = tooltip
        self.is_enabled = is_enabled
        self.mode = mode


_base_types.ShowCard.register(ShowCard)
_base_types.OpenUrl.register(OpenUrl)
_base_types.Submit.register(Submit)
_base_types.ToggleVisibility.register(ToggleVisibilty)
_base_types.Execute.register(Execute)