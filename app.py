from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

# Lista para almacenar los nodos conocidos
known_nodes = []


@app.route('/nodes', methods=['GET'])
def get_nodes():
    return jsonify(known_nodes)


@app.route('/add_node', methods=['POST'])
def add_node():
    node = request.get_json()
    if 'address' in node and 'port' in node:
        node_url = f"http://{node['address']}:{node['port']}"
        known_nodes.append(node_url)
        return jsonify({'message': 'Node added successfully'})
    else:
        return jsonify({'message': 'Invalid node data'}), 400

if __name__ == '__main__':
    self_node_url = 'http://localhost:8083'
    known_nodes.append(self_node_url)
    app.run(host='0.0.0.0', port=8083)