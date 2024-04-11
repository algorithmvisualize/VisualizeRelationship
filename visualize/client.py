import requests
from .params import *

def visualize(data, graph_type: int, graph_name: str=None, port=port):
    if graph_type != 3:
        data = [d for d in data if d[0] != d[1]]
    url = f'http://{address}:{port}/visualize'
    all_data = {
        'data': data,
        'graph_type': graph_type,
        'graph_name': graph_name
    }

    response = requests.post(url, json=all_data)
    if response.status_code == 200:
        # print(response.text)
        pass
    else:
        print('请求失败，状态码：', response.status_code)

if __name__ == '__main__':
    visualize(data, 1, "graph1")
    visualize(data, 2, "graph2")
    visualize({"data": data, "core": "Philip II"}, 3, "graph3")


