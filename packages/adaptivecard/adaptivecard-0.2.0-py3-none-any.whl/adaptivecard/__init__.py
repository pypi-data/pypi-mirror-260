from typing import Any, Literal, overload
from adaptivecard._mixin import Mixin
import adaptivecard._base_types as _base_types
from adaptivecard._typing import ListLike, DefaultNone, ElementList




class Content(Mixin):
    """Content é o elemento que recebe o AdaptiveCard e é adicionado à lista atachments, atributo de Message"""
    __slots__ = ("content_type", "content")
    def __init__(self, content: _base_types.AdaptiveCard):
        self.content_type = "application/vnd.microsoft.card.adaptive"
        self.content = content


class Message(Mixin):
    """"Estrutura de mensagem. Um card precisa estar contido em uma mensagem para ser enviado via Teams."""
    __slots__ = ('type', 'attachments')
    def __init__(self, attachments: ListLike[_base_types.Content] = DefaultNone):
        self.type = "message"
        if attachments is DefaultNone:
            attachments = []
        self.attachments = list(attachments)

    def attach(self, content):
        self.attachments.append(content)


class AdaptiveCard(Mixin):
    """O template principal do card"""  # Essas descrições hão de ficar mais detalhadas à medida que eu desenvolver a lib e sua documentação
    __slots__ = ("type", "version", "schema", "body", "actions", "fallback_text", "background_image", "min_height",
                 "rtl", "speak", "lang", "vertical_content_alignment")
    def __init__(self,
                 version: str | float = "1.2",
                 body: _base_types.Element | ListLike[_base_types.Element] = DefaultNone,
                 actions: _base_types.Action | ListLike[_base_types.Action] = DefaultNone,
                 fallback_text: str = DefaultNone,
                 background_image: str = DefaultNone,
                 min_height: str = DefaultNone,
                 rtl: bool = DefaultNone,
                 speak: str = DefaultNone,
                 lang: str = DefaultNone,
                 vertical_content_alignment: Literal["top", "center", "bottom"] = DefaultNone):
        
        self.type = "AdaptiveCard"
        self.version = version  
        self.schema = "http://adaptivecards.io/schemas/adaptive-card.json"
        if body is DefaultNone:
            body = ElementList()
        self.body: ElementList = body
        self.actions = actions
        self.fallback_text = fallback_text
        self.background_image = background_image
        self.min_height = min_height
        self.rtl = rtl
        self.speak = speak
        self.lang = lang
        self.vertical_content_alignment = vertical_content_alignment

    @property
    def empty(self):
        return len(self.body) == 0

    def append(self, value: _base_types.Element, /):
        if not isinstance(value, _base_types.Element):
            raise TypeError("Can only append an Element")
        self.body.append(value)

    def append_action(self, action: _base_types.Action, /):
        if not isinstance(action, _base_types.Action):
            raise TypeError("Can only append an Action")
        if not hasattr(self, 'actions'):
            self.actions = []
        self.actions.append(action)

    def to_message(self):
        content = Content(content=self)
        msg = Message(attachments=[content])
        return msg

    @overload
    def __getitem__(self, __i: int):
        ...

    @overload
    def __getitem__(self, __s: slice):
        ...

    def __getitem__(self, k):
        return self.body.__getitem__(k)
    
    def __setattr__(self, __name: str, __value: Any) -> None:
        if __name == 'version':
            version = __value
            if isinstance(version, float):
                version = str(version)
            __value = version
        if __name == 'body' and isinstance(__value, _base_types.Element) \
            or __name == 'actions' and isinstance(__value, _base_types.Action):
            __value = ElementList([__value])
        return super().__setattr__(__name, __value)
    

_base_types.AdaptiveCard.register(AdaptiveCard)
_base_types.Content.register(Content)
_base_types.Message.register(Message)
