import pytest
from adaptivecard.inputs import Text, Number, Date, Time, Toggle, Choice, ChoiceSet
from adaptivecard.exceptions import *


class Test:
    def test_text(self):
        input_text = Text(id="some id", is_multiline=True)
        with pytest.raises(TypeCheckError):
            input_text.spacing = "pading"
        assert isinstance(input_text.to_dict(), dict)

    def test_number(self):
        input_number = Number(id="some id")
        with pytest.raises(TypeCheckError):
            input_number.max = 3.4
        input_number.is_visible = True
        assert isinstance(input_number.to_dict(), dict)

    def test_date(self):
        input_date = Date(id="some id", max="2022-01-05", label="some label")

    def test_time(self):
        input_time = Time(id="some id", height="stretch", placeholder="some placeholder")
        with pytest.raises(TypeCheckError):
            input_time.fallback = 2
        input_time.spacing = None
        assert isinstance(input_time.to_dict(), dict)
    
    def test_toggle(self):
        input_toggle = Toggle(title="some title", id="some id")
        with pytest.raises(TypeCheckError):
            input_toggle.value = 3

    def test_choice_set(self):
        input_choice_set = ChoiceSet(id="some id", wrap=True, label="some lable")
        input_choice_set.choices = Choice(title="some title", value="some value")
        assert isinstance(input_choice_set.choices, list)