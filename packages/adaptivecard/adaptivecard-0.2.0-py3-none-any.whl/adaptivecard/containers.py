from typing import Any, Literal, overload
from sys import maxsize
import adaptivecard._base_types as _base_types
from adaptivecard._mixin import Mixin
from adaptivecard.card_elements import TextBlock
from adaptivecard._utils import convert_to_pixel_string, raise_invalid_pixel_error
from adaptivecard._typing import ListLike, DefaultNone, ElementList, ColumnList, RowList
from tabulate import tabulate



class Container(Mixin):
    """A grouping of elements. Containers are useful for grouping a number of related elements
    into one structure. All elements inside a container will inherit its styling attributes
    upon rendering of the card."""
    __slots__ = ('type', 'items', 'style', 'vertical_content_alignment', 'bleed', 'min_height',
                 'rtl', 'height', 'separator', 'spacing', 'id', 'is_visible')
    def __init__(self,
                 items: _base_types.Element | ListLike[_base_types.Element] = DefaultNone,
                 style: Literal["default", "emphasis", "good", "attention", "warning", "accent"] = DefaultNone,
                 vertical_content_alignment: Literal["top", "center", "bottom"] = DefaultNone,
                 bleed: bool = DefaultNone,
                 min_height: str | int = DefaultNone,
                 rtl: bool = DefaultNone,
                 height: Literal["auto", "stretch"] = DefaultNone,
                 separator: bool = DefaultNone,
                 spacing: Literal["default", "none", "small", "medium", "large", "extraLarge",
                                  "padding"] | None = DefaultNone,
                 id: str = DefaultNone,
                 is_visible: bool = DefaultNone):

        self.type = "Container"
        if items is DefaultNone:
            items = ElementList()
        self.items: ElementList = items
        self.style = style
        self.vertical_content_alignment = vertical_content_alignment
        self.bleed = bleed
        self.min_height = min_height
        self.rtl = rtl
        self.height = height
        self.separator = separator
        self.spacing = spacing
        self.id = id
        self.is_visible = is_visible

    @property
    def empty(self):
        return len(self.items) == 0

    def append(self, element: _base_types.Element):
        self.items.append(element)

    def __iter__(self):
        return iter(self.items)

    @overload
    def __getitem__(self, __i: int):
        ...

    @overload
    def __getitem__(self, __s: slice):
        ...

    def __getitem__(self, k):
        return self.items.__getitem__(k)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(items={self.items})"

    def __str__(self) -> str:
        return "[" + ", ".join([str(item) for item in self.items]) + "]"
    
    def __setattr__(self, __name: str, __value: Any) -> None:
        if __name == 'items':
            if isinstance(__value, ListLike):
                __value = ElementList(__value)
            elif isinstance(__value, _base_types.Element):
                __value = ElementList([__value])
        elif __name == "min_height":
            try:
                __value = convert_to_pixel_string(__value)
            except ValueError:
                raise_invalid_pixel_error()
        return super().__setattr__(__name, __value)


class Column(Mixin):
    """A column container. Columns must be grouped inside a ColumnSet."""
    __slots__ = ('type', 'items', 'background_image', 'bleed', 'fallback', 'min_height',
                 'rtl', 'separator', 'spacing', 'style', 'vertical_content_alignment', 'rtl',
                 'width', 'id', 'is_visible')
    def __init__(self,
                 items: _base_types.Element | ListLike[_base_types.Element | Any] | Any = DefaultNone,
                 background_image = DefaultNone,
                 bleed: bool = DefaultNone,
                 fallback: "Column" = DefaultNone,
                 min_height: str | int = DefaultNone,
                 rtl: bool = DefaultNone,
                 separator: bool = DefaultNone,
                 spacing: Literal["default", "none", "small", "medium", "large", "extraLarge",
                                  "padding"] | None = DefaultNone,
                 select_action: _base_types.Execute | _base_types.OpenUrl | _base_types.Submit
                   | _base_types.ToggleVisibility = DefaultNone,
                 style: Literal["default", "emphasis", "good", "attention", "warning",
                                "accent"] = DefaultNone,
                 vertical_content_alignment: Literal["top", "center", "bottom"] = DefaultNone,
                 width: str | int = DefaultNone,
                 id: str = DefaultNone,
                 is_visible: bool = DefaultNone):

        self.type = "Column"
        if items is DefaultNone:
            items = ElementList()
        self.items: ElementList = items
        self.background_image = background_image
        self.bleed = bleed
        self.fallback = fallback
        self.min_height = min_height
        self.rtl = rtl
        self.separator = separator
        self.spacing = spacing
        self.select_action = select_action
        self.style = style
        self.vertical_content_alignment = vertical_content_alignment
        self.width = width
        self.id = id
        self.is_visible = is_visible

    def append(self, value: _base_types.Element | Any):
        if not isinstance(value, _base_types.Element):
            value = TextBlock(value)
        self.items.append(value)

    def __iter__(self):
        return iter(self.items)
    
    def __getitem__(self, __i, /):
        return self.items.__getitem__(__i)
    
    def __setitem__(self, __key, __value, /):
        return self.items.__setitem__(__key, __value)
    
    def __str__(self):
        return str([str(item) for item in self.items])
    
    def __repr__(self):
        return f"{self.__class__.__name__}({self.items})"

    def __setattr__(self, __name: str, __value: Any) -> None:
        if __name == "items":
            if isinstance(__value, _base_types.Element):
                __value = ElementList([__value])
            elif isinstance(__value, ListLike):
                __value = ElementList([item 
                                 if isinstance(item, _base_types.Element) 
                                 else TextBlock(item)
                                 for item in __value])
            else:
                __value = ElementList([TextBlock(__value)])
        elif __name == "min_height" or __name == "width":
            try:
                __value = convert_to_pixel_string(__value)
            except ValueError:
                raise_invalid_pixel_error(__name, __value)
        return super().__setattr__(__name, __value)


class ColumnSet(Mixin):
    """A container for columns."""
    __slots__ = ('type', 'columns', 'style', 'bleed', 'min_height', 'horizontal_alignment', 'height',
                 'separator', 'spacing', 'id', 'is_visible')
    def __init__(self,
                 columns: ListLike[Column | ListLike[Any]] = DefaultNone,
                 select_action: _base_types.Execute | _base_types.OpenUrl | _base_types.Submit
                   | _base_types.ToggleVisibility = DefaultNone,
                 style: Literal["default", "emphasis", "good", "attention", "warning",
                                "accent"] = DefaultNone,
                 bleed: bool = DefaultNone,
                 min_height: str | int = DefaultNone,
                 horizontal_alignment: Literal["left", "center", "right"] | None = DefaultNone,
                 fallback: _base_types.Element = DefaultNone,
                 height: Literal["auto", "stretch"] | None = DefaultNone,
                 separator: bool | None = DefaultNone,
                 spacing: Literal["default", "none", "small", "medium", "large", "extraLarge",
                                  "padding"] | None = DefaultNone,
                 id: str = DefaultNone,
                 is_visible: bool = DefaultNone):

        self.type = 'ColumnSet'
        if columns is DefaultNone:
            columns = ColumnList()
        self.columns: ColumnList = columns
        self.style = style
        self.bleed = bleed
        self.min_height = min_height
        self.horizontal_alignment = horizontal_alignment
        self.height = height
        self.separator = separator
        self.spacing = spacing
        self.id = id
        self.is_visible = is_visible

    def append(self, column: Column | ListLike):
        if not isinstance(column, (Column, ListLike)):
            raise TypeError(f"Expected Column or list-like object, got {type(column).__name__} instead")
        if not isinstance(column, Column):
            column = Column(column)
        self.columns.append(column)

    def __iter__(self):
        return iter(self.columns)

    @overload
    def __getitem__(self, __i: int):
        ...

    @overload
    def __getitem__(self, __s: slice):
        ...

    def __getitem__(self, __k, /):
        return self.columns.__getitem__(__k)
    
    def __setitem__(self, __key: int, __value: object, /):
        if not isinstance(__value, Column):
            raise TypeError()
        return self.columns.__setitem__(__key, __value)
    
    def __repr__(self):
        return f"{self.__class__.__name__}({self.columns})"
    
    def __str__(self):
        return "[" + ", ".join([str(col) for col in self.columns]) + "]"

    def __setattr__(self, __name: str, __value: Any) -> None:
        if __name == "columns":
            if not isinstance(__value, ListLike):
                __value = [__value]
            columns = []
            for col in __value:
                if not isinstance(col, _base_types.Element):
                    col = TextBlock(col)
                if not isinstance(col, Column):
                    col = Column(col)
                columns.append(col)
            __value = ColumnList(columns)
        elif __name == "min_height":
            try:
                __value = convert_to_pixel_string(__value)
            except ValueError:
                raise_invalid_pixel_error(__name, __value)
        return super().__setattr__(__name, __value)


class TableCell(Mixin):
    __slots__ = ('type', 'items', 'select_action', 'style', 'vertical_alignment', 'bleed',
                 'background_image', 'min_height', 'rtl')
    def __init__(self,
                 items: Any | ListLike[Any] = DefaultNone,
                 select_action: _base_types.Execute | _base_types.OpenUrl | _base_types.Submit
                 | _base_types.ToggleVisibility = DefaultNone,
                 style: Literal["default", "emphasis", "good", "attention", "warning",
                                "accent"] = DefaultNone,
                 vertical_alignment: Literal["top", "center", "bottom"] = DefaultNone,
                 bleed: bool = DefaultNone,
                 background_image: str = DefaultNone,
                 min_height: str | int = DefaultNone,
                 rtl: bool = DefaultNone):

        self.type = "TableCell"
        if items is DefaultNone:
            items = ElementList()
        self.items: ElementList = items
        self.select_action = select_action
        self.items = items
        self.style = style
        self.vertical_alignment = vertical_alignment
        self.bleed = bleed
        self.background_image = background_image
        self.min_height = min_height
        self.rtl = rtl

    def append(self, item: _base_types.Element | Any):
        if not isinstance(item, _base_types.Element):
            item = TextBlock(item)
        self.items.append(item)

    def squeeze(self):
        ...

    @overload
    def __getitem__(self, __i: int):
        ...

    @overload
    def __getitem__(self, __s: slice):
        ...

    def __getitem__(self, __k, /):
        return self.items.__getitem__(__k)
    
    def __setitem__(self, __key, __value, /):
        if not isinstance(__value, _base_types.Element):
            raise TypeError
        return self.items.__setitem__(__key, __value)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(items={[item for item in self.items]})"

    def __str__(self) -> str:
        return "[" + ", ".join([str(item) for item in self.items]) + "]"

    def __iter__(self):
        return iter(self.items)
    
    def __setattr__(self, __name: str, __value: Any) -> None:
        if __name == "items":
            items = __value
            if isinstance(items, _base_types.Element):
                items = ElementList([items])
            elif isinstance(items, ListLike):
                if not isinstance(items, ElementList):
                    items = ElementList([item
                                if isinstance(item, _base_types.Element)
                                else TextBlock(item)
                                for item in items])
            else:
                items = ElementList([TextBlock(items)])
            __value = items
        elif __name == "min_height":
            min_height = __value
            try:
                min_height = convert_to_pixel_string(min_height)
            except ValueError:
                raise_invalid_pixel_error(__name, min_height)
            __value = min_height
        return super().__setattr__(__name, __value)


class TableRow(Mixin):
    __slots__ = ("type", "cells", "style")
    def __init__(self,
                 cells: ListLike[Any] = DefaultNone,
                 style: Literal["default", "emphasis", "good", "attention", "warning",
                                "accent"] = DefaultNone):
        self.type = "TableRow"
        if cells is DefaultNone:
            cells = ElementList()
        self.cells = cells
        self.style = style
    
    def append(self, __object: _base_types.Element | Any, /):
        if not isinstance(__object, TableCell): __object = TableCell(__object)
        self.cells.append(__object)

    @overload
    def __getitem__(self, __i: int):
        ...

    @overload
    def __getitem__(self, __s: slice):
        ...

    def __getitem__(self, __k):
        if isinstance(__k, slice):
            return self.__class__(cells=self.cells[__k])
        return self.cells.__getitem__(__k)
    
    def __setitem__(self, __key, __value):
        if not isinstance(__value, TableCell): __value = TableCell(__value)
        self.cells.__setitem__(__key, __value)

    def __contains__(self, value):
        return value in self.cells
    
    def __setattr__(self, __name: str, __value: Any) -> None:
        if __name == "cells":
            cells = __value
            if not isinstance(cells, ListLike):
                raise TypeError
            cells = ElementList([TableCell(cell) if not isinstance(cell, TableCell) else cell
                           for cell in cells])
            __value = cells
        return super().__setattr__(__name, __value)

    def __len__(self):
        return len(self.cells)

    def __iter__(self):
        return iter(self.cells)
    
    def index(self, value=1, start: int = 0, stop: int = maxsize, /):
        return self.cells.index(value, start, stop)

    def count(self, value, /):
        return self.cells.count(value)
    
    def __reversed__(self):
        attrs = {attr_name: getattr(self, attr_name)
                 if attr_name != "cells"
                 else reversed(getattr(self, attr_name))
                 for attr_name in self.__slots__
                 if hasattr(self, attr_name)}
        return self.__class__(**attrs)

    def __repr__(self):
        return f"{self.__class__.__name__}({str(self.cells)})"

    def __str__(self):
        return "[" + ", ".join([str(cell) for cell in self.cells]) + "]"


class Table(Mixin):
    __slots__ = ('type', 'columns', 'rows', 'first_row_as_header', 'show_grid_lines', 'grid_style',
                 'horizontal_cell_content_alignment', 'vertical_cell_content_alignment', 'fallback', 'height',
                 'separator', 'spacing', 'id', 'is_visible')
    def __init__(self,
                 rows: ListLike[ListLike] = DefaultNone,
                 first_row_as_header: bool = DefaultNone,
                 columns: ListLike[int] = DefaultNone,
                 show_grid_lines: bool = DefaultNone,
                 grid_style: Literal["default", "emphasis", "good", "attention", "warning",
                                     "accent"] = DefaultNone,
                 horizontal_cell_content_alignment: Literal["left", "center", "right"] = DefaultNone,
                 vertical_cell_content_alignment: Literal["top", "center", "bottom"] = DefaultNone,
                 fallback: _base_types.Element = DefaultNone,
                 height: Literal["auto", "stretch"] = DefaultNone,
                 separator: bool = DefaultNone,
                 spacing: Literal["default", "none", "small", "medium", "large", "extraLarge",
                                  "padding"] | None = DefaultNone,
                 id: str = DefaultNone,
                 is_visible: bool = DefaultNone):

        self.type = "Table"
        if rows is DefaultNone:
            rows = []
        self.rows: RowList = rows
        self.columns = columns if columns is not None else []
        self.first_row_as_header = first_row_as_header
        self.show_grid_lines = show_grid_lines
        self.grid_style = grid_style
        self.horizontal_cell_content_alignment = horizontal_cell_content_alignment
        self.vertical_cell_content_alignment = vertical_cell_content_alignment
        self.fallback = fallback
        self.height = height
        self.separator = separator
        self.spacing = spacing
        self.id = id
        self.is_visible = is_visible

    @overload
    def __getitem__(self, __i: int):
        ...

    @overload
    def __getitem__(self, __s: slice):
        ...

    def __getitem__(self, __k, /):
        return self.rows.__getitem__(__k)
    
    def __setitem__(self, __key, __value, /):
        if not isinstance(__value, TableRow):
            raise TypeError
        return self.rows.__setitem__(__key, __value)
    
    def append(self, row: ListLike):
        if not isinstance(row, ListLike):
            raise TypeError
        if not isinstance(row, TableRow):
            row = TableRow(row)
        self.rows.append(row)
    
    # custom to_dict para lidar com o formato atípico do atributo columns dentro do json
    def to_dict(self):
        dic = super().to_dict()
        if hasattr(self, "columns") and self.columns:
            json_columns = [{"width": width} for width in self.columns]
        elif self.rows:
            json_columns = [{"width": 1} for _ in self.rows[0]]
        else:
            json_columns = dic["columns"]
        dic["columns"] = json_columns
        return dic
    
    def __len__(self):
        return len(self.rows)
    
    def __str__(self):
        rows = [["\n".join([str(item) for item in cell.items]) for cell in row.cells] for row in self.rows]
        if getattr(self, "first_row_as_header", False) and self.rows:
            headers, *rows = rows
            return tabulate(rows, headers, tablefmt='grid')

        return tabulate(rows, tablefmt='grid')

    def __iter__(self):
        return iter(self.rows)

    def __setattr__(self, __name: str, __value: Any) -> None:
        if __name == "rows":
            rows = __value
            if not isinstance(rows, ListLike) or \
            not all([isinstance(item, ListLike) for item in rows]):
                raise TypeError("argument 'rows' must be a collection of collections")
            rows = RowList([TableRow(row) for row in rows])
            __value = rows
        return super().__setattr__(__name, __value)


class ActionSet(Mixin):
    __slots__ = ("type", "actions", "fallback", "height", "separator", "spacing", "id", "is_visible")
    def __init__(self,
                 actions: _base_types.Action | ListLike[_base_types.Action] = DefaultNone,
                 fallback: _base_types.Element = DefaultNone,
                 height: Literal["auto", "stretch"] = DefaultNone,
                 separator: bool = DefaultNone,
                 spacing: Literal["default", "none", "small", "medium", "large", "extraLarge",
                                  "padding"] | None = DefaultNone,
                 id: str = DefaultNone,
                 is_visible: bool = DefaultNone
                 ):
        self.type = "ActionSet"
        if actions is DefaultNone:
            actions = ElementList()
        self.actions: ElementList = actions
        self.fallback = fallback
        self.height = height
        self.separator = separator
        self.spacing = spacing
        self.id = id
        self.is_visible = is_visible

    @overload
    def __getitem__(self, __i: int):
        ...

    @overload
    def __getitem__(self, __s: slice):
        ...

    def __getitem__(self, __k):
        r = self.actions.__getitem__(__k)  
        if isinstance(__k, slice):
            r = self.__class__(r)
        return r

    def append(self, action: _base_types.Action) -> None:
        if not isinstance(action, _base_types.Action):
            raise TypeError("Can only append objetcs of type Action")
        self.actions.append(action)

    def __setattr__(self, __name: str, __value: Any) -> None:
        if __name == "actions":
            if isinstance(__value, _base_types.Action):
                __value = ElementList([__value])
            elif isinstance(__value, ListLike):
                __value = ElementList(__value)
        return super().__setattr__(__name, __value)
        

_base_types.Container.register(Container)
_base_types.Column.register(Column)
_base_types.ColumnSet.register(ColumnSet)
_base_types.Table.register(Table)
_base_types.TableRow.register(TableRow)
_base_types.TableCell.register(TableCell)
_base_types.ActionSet.register(ActionSet)