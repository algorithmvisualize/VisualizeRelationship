import requests
from .params import *

def visualize(data, graph_type: int, graph_name: str=None, port=port):
    """
    Visualize the data in a graph
    :param data: data to be visualized.
     For graph 1 or graph2, specify the structure of `data` in `params.py`;
     For graph 3, arrange data as `{"data": `data`, "core": core, "type": type}`,
        `data` is the same as graph1 and graph2, core is the entity in `data`.
        type is optional, if type is None, then show both NEG and POS, otherwise choose NEG or POS
    :param graph_type: The type of graph to visualize, support type in [1, 2, 3]
    :param graph_name: The name of the graph to visualize, default value is f'graph{graph_type}'
    :param port: The port to connect to server
    """
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
        print('wrong code: ', response.status_code)

if __name__ == '__main__':
    visualize(data, 1, "graph1")
    visualize(data, 2, "graph2")
    visualize({"data": data, "core": "Philip II"}, 3, "graph3")


