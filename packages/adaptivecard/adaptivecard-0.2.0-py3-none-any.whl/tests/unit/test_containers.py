import pytest
from adaptivecard.containers import Container, ColumnSet, Column, Table, TableRow, ActionSet
from adaptivecard.exceptions import *


class Test:
    def test_container(self):
        container = Container()
        with pytest.raises(TypeCheckError):
            Container((1,2,3))
        with pytest.raises(ValueCheckError):
            container.style = "wrong value"
        with pytest.raises(AttributeError):
            container.wrong_attribute = "value"

    def test_column_set(self):
        column_set = ColumnSet()
        with pytest.raises(TypeCheckError):
            column_set.horizontal_alignment = "Left"
        with pytest.raises(ValueError):
            column_set.min_height = "20pc"
        column_set.min_height = 20
        assert column_set.min_height == "20px"

    def test_table(self):
        table = Table()
        table.append([1, 2, 3])
        assert all([isinstance(row, TableRow) for row in table])

    def test_table_row(self):
        table_row = TableRow(cells=[1,2,3])
        assert table_row[2][0].text == '3'
        with pytest.raises(ValueCheckError):
            table_row.style = "wrong style"
    
    def test_action_set(self):
        action_set = ActionSet()
        with pytest.raises(TypeError):
            action_set.append("some text")
        with pytest.raises(AttributeError):
            action_set.wrong_attribute = 2

    def test_to_dict(self):
        container = Container()
        columns = [Column("some text"), Column("some other text")]
        column_set = ColumnSet(columns)
        container.append(column_set)
        assert isinstance(container.to_dict(), dict)