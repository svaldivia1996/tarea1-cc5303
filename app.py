from flask import Flask, jsonify, request
import requests
import os

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
        if node_url not in known_nodes:
            known_nodes.append(node_url)

            # Envía una solicitud POST al nuevo nodo para que también lo agregue a su lista
            try:
                requests.post(f"{node_url}/add_node", json={'address': os.getenv('ADDRESS', 'localhost'), 'port': os.getenv('PORT', '8083')})
            except requests.exceptions.RequestException:
                pass
            return jsonify({'message': 'Node added successfully'})
        
    else:
        return jsonify({'message': 'Invalid node data'}), 400


def connect_to_known_node(node_url):
    try:
        response = requests.get(f"{node_url}/nodes")
        if response.status_code == 200:
            nodes = response.json()
            for node in nodes:
                if node not in known_nodes:
                    known_nodes.append(node)
    except requests.exceptions.RequestException:
        pass


if __name__ == '__main__':
    self_node_url = f"http://localhost:{os.getenv('PORT', '8083')}"
    known_nodes.append(self_node_url)

    # Conectarse a los nodos conocidos
    for node_url in known_nodes:
        if node_url != self_node_url:
            connect_to_known_node(node_url)

    app.run(host='0.0.0.0', port=8083)