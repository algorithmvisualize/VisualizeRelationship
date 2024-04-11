import json

from visualize.client import visualize
with open("data.json", "r", encoding="utf-8") as f:
    texts = json.load(f)
from visualize.params import data

# for text in texts:
#     visualize(texts[text], 2)

a = set()
for d in data:
    a.add(d[0])
    a.add(d[1])
for a1 in a:
    visualize({"data": data, "core": a1, "type": "NEG"}, 3)

