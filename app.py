from flask import Flask, jsonify, request
import redis

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
        known_nodes.append(f"http://{node['address']}:{node['port']}")
        announce_node_to_known_nodes(node['address'], node['port'])
        return jsonify({'message': 'Node added successfully'})
    else:
        return jsonify({'message': 'Invalid node data'}), 400
    
def announce_node_to_known_nodes(address, port):
    for known_node in known_nodes:
        try:
            url = f"http://{known_node}/add_node"
            payload = {'address': address, 'port': port}
            response = requests.post(url, json=payload)
            response.raise_for_status()
        except requests.exceptions.RequestException:
            # Manejar el caso si la solicitud falla
            pass

if __name__ == '__main__':
    self_node_url = 'http://localhost:8083'
    known_nodes.append(self_node_url)
    app.run(host='0.0.0.0', port=8083)
