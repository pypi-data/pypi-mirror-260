from adaptivecard import AdaptiveCard
from adaptivecard.containers import Container, ColumnSet, Column, Table, TableRow
from adaptivecard.card_elements import TextBlock, Image


class Test:
    def test_message(self):
        card = AdaptiveCard()
        container = Container(style='warning', bleed=True, min_height=10)
        columns = [Column([1,1,1]), Column([2,2,2])]
        column_set = ColumnSet((columns), style='warning', min_height=8, height='auto')
        container.append(column_set)
        card.append(container)
        container_2 = Container()
        table = Table(first_row_as_header=True)
        table.append([1, 2, TextBlock("header", style='heading', weight='bolder')])
        row_2 = TableRow([4,5,6])
        table.append(row_2)
        assert table[1][0][0].text == "4"
        table[1][0] = 100
        assert table[1][0][0].text == "100"
        container_2.append(table)
        card.append(container_2)
        img = Image("https://hips.hearstapps.com/hmg-prod/images/dog-puppy-on-garden-royalty-free-image-1586966191.jpg?crop=1xw:0.74975xh;center,top&resize=1200:*",
                    size='medium', style='person', separator=True, height=70)
        card.append(img)
        msg = card.to_message()
        json = msg.to_dict()
        assert isinstance(json, dict)