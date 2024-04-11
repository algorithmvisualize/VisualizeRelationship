import json

res1 = {}
list_fifo = ['Philip II']
deprecate_list = []
num = 0

with open("data.json", "r", encoding="utf-8") as f:
    induction = json.load(f)
data = induction['Battle of Chaeronea (338 BC)']
type = "NEG"
res = {}
def union_person(data, list_fifo, type, res, deprecate_list=None, num=0):
    if not list_fifo:
        return

    if not deprecate_list:
        deprecate_list = []

    if num not in res:
        res[num]=[]

    for _ in range(len(list_fifo)):
        entity = list_fifo.pop()
        deprecate_list.append(entity)

        for ent in data:
            if ent[0] == entity and ent[1] not in deprecate_list:
                if ent[3] == "REL":
                    list_fifo.append(ent[1])
                    if ent[1] not in list_fifo:
                        deprecate_list.append(ent[1])
                elif ent[3] == type:
                    res[num].append(ent[1])
                    deprecate_list.append(ent[1])
            elif ent[1] == entity and ent[0] not in deprecate_list:
                if ent[3] == "REL":
                    list_fifo.append(ent[0])
                    if ent[0] not in list_fifo:
                        deprecate_list.append(ent[0])
                elif ent[3] == type:
                    res[num].append(ent[0])
                    deprecate_list.append(ent[0])

    if not res[num]:
        res.pop(num)



union_person(data, list_fifo, type, res, deprecate_list, num + 1)
print(res)
