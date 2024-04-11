from flask import Flask, jsonify, request, render_template
import threading
import uuid
from .pyqt import start
import logging
from .params import *
from flask_cors import CORS
log = logging.getLogger('werkzeug')
log.disabled = True
app = Flask(__name__, static_url_path='/static')
CORS(app)
data_store = {}
is_start = False
app_lock = threading.Lock()
all_port = port
"""
render html
"""
@app.route('/')
def index():
    graph_type = request.args.get('graph_type')
    return render_template(f'graph{graph_type}.html')


@app.route('/test')
def test():
    return 'Test route is working'


@app.route('/data')
def get_data():
    id = request.args.get('id')
    if id in data_store:
        return jsonify(data_store[id])
    else:
        return jsonify({'error': 'Invalid ID'}), 404


@app.route("/visualize", methods=['POST'])
def visualize():
    data = request.json.get('data')
    graph_type = request.json.get('graph_type')
    name = request.json.get('graph_name')

    open_browser(data, graph_type, name)
    return "ok"


def open_browser(data, graph_type, name=None):
    if name is None:
        name = f'graph{graph_type}'
    start_server()
    # open_browser_shadow(data, graph_type, name)
    threading.Timer(0.01, open_browser_shadow, args=(data, graph_type, name)).start()  # 延迟打开浏览器，确保服务器已启动


def open_browser_shadow(data, graph_type, name):
    id = uuid.uuid4()
    with app_lock:
        data_store[str(id)] = {'value': data}
    url = f'http://{address}:{all_port}/?data_id={id}&graph_type={graph_type}'
    if "type" in data:
        url = f'{url}&type'
    # print(f'search your {name} on {url}')
    start(url, f'{name}')



def start_server(port=port):
    """
    start visualization server
    """
    global is_start
    with app_lock:

        if not is_start:
            threading.Thread(target=run, args=(port, )).start()
            is_start = True


def run(port=port):
    global all_port
    all_port = port
    app.run(debug=False, port=port)


# check work of server
if __name__ == '__main__':
    name = "_1"
    start_server()
