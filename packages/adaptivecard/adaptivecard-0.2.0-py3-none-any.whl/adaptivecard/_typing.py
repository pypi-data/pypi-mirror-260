from typing import Protocol, Sequence, Iterator, Iterable, TypeVar, Any, SupportsIndex, overload, runtime_checkable
from adaptivecard._base_types import Element, Choice, TableRow, Column


_T_co = TypeVar("_T_co", covariant=True)

@runtime_checkable
class SequenceNotStr(Protocol[_T_co]):
    @overload
    def __getitem__(self, index: SupportsIndex, /) -> _T_co:
        ...

    @overload
    def __getitem__(self, index: slice, /) -> Sequence[_T_co]:
        ...

    def __contains__(self, value: object, /) -> bool:
        ...

    def __len__(self) -> int:
        ...

    def __iter__(self) -> Iterator[_T_co]:
        ...

    def index(self, value: Any, start: int = ..., stop: int = ..., /) -> int:
        ...

    def count(self, value: Any, /) -> int:
        ...

    def __reversed__(self) -> Iterator[_T_co]:
        ...

ListLike = SequenceNotStr

DefaultNone = object()


class ElementList(list):
    def __init__(self, data=None) -> None:
        if data is None: data = []
        super().__init__(data)
    def append(self, __object) -> None:
        if not isinstance(__object, Element):
            raise TypeError(f"{type(self).__name__} only accepts items of type {Element.__name__}")
        return super().append(__object)
    def insert(self, __index: SupportsIndex, __object: Any) -> None:
        if not isinstance(__object, Element):
            raise TypeError(f"{type(self).__name__} only accepts items of type {Element.__name__}")
        return super().insert(__index, __object)
    def __setitem__(self, __key, __value, /):
        if not isinstance(__value, Element):
            raise TypeError(f"{type(self).__name__} only accepts items of type {Element.__name__}")
        return super().__setitem__(__key, __value)
    @overload
    def __getitem__(self, __i: int):
        ...
    @overload
    def __getitem__(self, __s: slice):
        ...
    def __getitem__(self, k):
        r = super().__getitem__(k)
        if isinstance(r, list):
            r = self.__class__(r)
        return r


class ColumnList(list):
    def __init__(self, data=None) -> None:
        if data is None: data = []
        super().__init__(data)
    def append(self, __object) -> None:
        if not isinstance(__object, Column):
            raise TypeError(f"{type(self).__name__} only accepts items of type {Column.__name__}")
        return super().append(__object)
    def insert(self, __index: SupportsIndex, __object: Any) -> None:
        if not isinstance(__object, Column):
            raise TypeError(f"{type(self).__name__} only accepts items of type {Column.__name__}")
        return super().insert(__index, __object)
    def __setitem__(self, __key, __value, /):
        if not isinstance(__value, Column):
            raise TypeError(f"{type(self).__name__} only accepts items of type {Column.__name__}")
        return super().__setitem__(__key, __value)
    @overload
    def __getitem__(self, __i: int):
        ...
    @overload
    def __getitem__(self, __s: slice):
        ...
    def __getitem__(self, k):
        r = super().__getitem__(k)
        if isinstance(r, list):
            r = self.__class__(r)
        return r


class RowList(list):
    def __init__(self, data=None) -> None:
        if data is None: data = []
        super().__init__(data)
    def append(self, __object) -> None:
        if not isinstance(__object, TableRow):
            raise TypeError(f"{type(self).__name__} only accepts items of type {TableRow.__name__}")
        return super().append(__object)
    def insert(self, __index: SupportsIndex, __object: Any) -> None:
        if not isinstance(__object, TableRow):
            raise TypeError(f"{type(self).__name__} only accepts items of type {TableRow.__name__}")
        return super().insert(__index, __object)
    def __setitem__(self, __key, __value, /):
        if not isinstance(__value, TableRow):
            raise TypeError(f"{type(self).__name__} only accepts items of type {TableRow.__name__}")
        return super().__setitem__(__key, __value)
    @overload
    def __getitem__(self, __i: int):
        ...
    @overload
    def __getitem__(self, __s: slice):
        ...
    def __getitem__(self, k):
        r = super().__getitem__(k)
        if isinstance(r, list):
            r = self.__class__(r)
        return r


class ChoiceList(list):
    def __init__(self, data=None) -> None:
        if data is None: data = []
        super().__init__(data)
    def append(self, __object) -> None:
        if not isinstance(__object, Choice):
            raise TypeError(f"{type(self).__name__} only accepts items of type {Choice.__name__}")
        return super().append(__object)
    def insert(self, __index: SupportsIndex, __object: Any) -> None:
        if not isinstance(__object, Choice):
            raise TypeError(f"{type(self).__name__} only accepts items of type {Choice.__name__}")
        return super().insert(__index, __object)
    def __setitem__(self, __key, __value, /):
        if not isinstance(__value, Choice):
            raise TypeError(f"{type(self).__name__} only accepts items of type {Choice.__name__}")
        return super().__setitem__(__key, __value)
    @overload
    def __getitem__(self, __i: int):
        ...
    @overload
    def __getitem__(self, __s: slice):
        ...
    def __getitem__(self, k):
        r = super().__getitem__(k)
        if isinstance(r, list):
            r = self.__class__(r)
        return r