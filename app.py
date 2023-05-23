from flask import Flask, jsonify, request

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
        known_nodes.append(f"{node['address']}:{node['port']}")
        return jsonify({'message': 'Node added successfully'})
    else:
        return jsonify({'message': 'Invalid node data'}), 400


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8083)
