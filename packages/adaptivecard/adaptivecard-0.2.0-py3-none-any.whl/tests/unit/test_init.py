import pytest
from adaptivecard import AdaptiveCard
from adaptivecard.card_elements import TextBlock
from adaptivecard.containers import Container
from adaptivecard.exceptions import *


class Test:
    def test_(self):
        card = AdaptiveCard()
        with pytest.raises(TypeCheckError):
            AdaptiveCard([1,2,3])
        with pytest.raises(TypeError):
            card.append("")
        with pytest.raises(TypeError):
            card.append_action("")
        with pytest.raises(TypeError):
            card.body.append(1)
        with pytest.raises(AttributeError):
            card.wrong_attribute = "value"
    def test_to_dict(self):
        card = AdaptiveCard(body=Container(TextBlock("some text"))).to_dict()
        assert isinstance(card, dict)
    def test__(self):
        assert AdaptiveCard().empty