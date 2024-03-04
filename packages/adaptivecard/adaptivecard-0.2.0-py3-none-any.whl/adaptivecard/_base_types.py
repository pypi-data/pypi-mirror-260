from abc import ABC



class Element(ABC):
    pass


class AdaptiveCard(ABC):
    pass


class ActionSet(ABC):
    pass


class Action(ABC):
    pass


class ShowCard(ABC):
    pass


class Execute(ABC):
    pass


class OpenUrl(ABC):
    pass


class Submit(ABC):
    pass


class ToggleVisibility(ABC):
    pass


class TableRow(ABC):
    pass


class TableCell(ABC):
    pass


class Content(ABC):
    pass


class Message(ABC):
    pass


class Container(ABC):
    pass


class ColumnSet(ABC):
    pass


class Column(ABC):
    pass


class Table(ABC):
    pass


class TextBlock(ABC):
    pass


class Image(ABC):
    pass


class Text(ABC):
    pass


class Number(ABC):
    pass


class Date(ABC):
    pass


class Time(ABC):
    pass


class Toggle(ABC):
    pass


class Choice(ABC):
    pass


class ChoiceSet(ABC):
    pass


Element.register(AdaptiveCard)
Element.register(Table)
Element.register(TableRow)
Element.register(TableCell)
Element.register(ColumnSet)
Element.register(Column)
Element.register(Container)
Element.register(TextBlock)
Element.register(Image)
Element.register(Message)
Element.register(Content)
Element.register(Action)
Element.register(ActionSet)
Action.register(ShowCard)
Action.register(Execute)
Action.register(OpenUrl)
Action.register(Submit)
Action.register(ToggleVisibility)
