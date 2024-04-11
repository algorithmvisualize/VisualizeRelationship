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
        visualize(data, 1)

    def test_graph2(self):
        visualize(data, 2)

    def test_graph3(self):
        visualize({"data": data, "core": "Philip II"}, 3, graph_name=f'graph3')

    def test_graph3_pos(self):
        visualize({"data": data, "core": "Philip II", "type": 'POS'}, 3, graph_name=f'graph3_POS')

    def test_graph3_neg(self):
        visualize({"data": data, "core": "Philip II", "type": 'NEG'}, 3, graph_name=f'graph3_POS')

    def test_graph1_multi(self):
        texts = load_data()
        for name in texts:
            visualize(texts[name], 1, graph_name=name)

    def test_graph2_multi(self):
        texts = load_data()
        for name in texts:
            visualize(texts[name], 2, graph_name=name)

    def test_graph3_multi(self):
        entities = all_entity_from_data(data)
        for entity in entities:
            visualize({"data": data, "core": entity}, 3, graph_name=f'graph3 entity={entity}')


if __name__ == "__main__":
    unittest.main()
