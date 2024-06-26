import json

from visualize.client import visualize
from visualize.params import data
import unittest


def load_data():
    with open("data.json", "r", encoding="utf-8") as f:
        texts = json.load(f)
    return texts


def all_entity_from_data(data: list):
    temp = set()
    [(temp.add(d[0]), temp.add(d[1]))for d in data]
    return list(temp)


class ClientTest(unittest.TestCase):

    def test_graph1(self):
        visualize(data, 1, "Battle of Chaeronea (338 BC)")

    def test_graph2(self):
        visualize(data, 2, "Battle of Chaeronea (338 BC)")

    def test_graph3(self):
        visualize({"data": data, "core": "Philip II"}, 3, graph_name=f'Philip II')

    def test_graph3_pos(self):
        visualize({"data": data, "core": "Philip II", "type": 'POS'}, 3, graph_name=f'Philip II_POS')

    def test_graph3_neg(self):
        visualize({"data": data, "core": "Philip II", "type": 'NEG'}, 3, graph_name=f'Philip II_NEG')

    def test_graph1_multi(self):
        texts = load_data()
        for name in texts:
            visualize(texts[name], 1, graph_name=name)

    def test_graph2_multi(self):
        texts = load_data()
        for name in texts:
            visualize(texts[name], 2, graph_name=name)

    def test_graph3_multi(self):
        show_graph3(data)


def show_graph3(data1: list, types=None):
    if types is None:
        types = ["POS", "NEG"]
    entities = all_entity_from_data(data1)
    for entity in entities:
        if len(types) == 2:
            visualize({"data": data1, "core": entity}, 3, graph_name=f'entity={entity}')
        else:
            visualize({"data": data1, "core": entity, "type": types[0]}, 3, graph_name=f'entity={entity}')


if __name__ == "__main__":
    unittest.main()
