from flask import Flask, jsonify, request
import requests
import os
import socket

app = Flask(__name__)

# Lista para almacenar los nodos conocidos
known_nodes = []

def get_container_ipv4_address():
    # Obtener el nombre de host del contenedor
    container_hostname = socket.gethostname()

    # Obtener la dirección IP del contenedor a partir del nombre de host
    container_ip = socket.gethostbyname(container_hostname)

    return container_ip

@app.route('/', methods=['GET'])
def hola():
    return jsonify({'message': 'Hola Mundo'})

@app.route('/nodes', methods=['GET'])
def get_nodes():
    return jsonify(known_nodes)


@app.route('/connect', methods=['POST'])
def connect_node():
    node = request.get_json()
    node_address = node.get('node_address')
    node_port = node.get('node_port')
    container_ipv4 = get_container_ipv4_address()

    try:
        response = requests.get(f'http://{node_address}:8080/nodes')
        node_list = response.json()
        self_node_url = f"http://{container_ipv4}:{os.getenv('PORT', '8080')}"

        for node in node_list:
            if node not in known_nodes:
                known_nodes.append(node)
                ip_nodo_vecino = node.split(':')[1].replace('//', '')
                requests.post(f'http://{ip_nodo_vecino}:8080/connect', json={'node_address': container_ipv4, 'node_port': os.getenv('PORT', '8080')})

        if (f'http://{node_address}:{node_port}') not in known_nodes:
            known_nodes.append(f'http://{node_address}:{node_port}')
            requests.post(f'http://{node_address}:8080/connect', json={'node_address': container_ipv4, 'node_port': os.getenv('PORT', '8080')})


    except requests.exceptions.ConnectionError:
        return 'Unable to connect', 400

    return jsonify(known_nodes), 200


if __name__ == '__main__':
    container_ipv4 = get_container_ipv4_address()  # Obtiene la dirección IPv4 del contenedor
    self_node_url = f"http://{container_ipv4}:{os.getenv('PORT', '8080')}"
    known_nodes.append(self_node_url)

    # Conectarse a los nodos conocidos
    """for node_url in known_nodes:
        if node_url != self_node_url:
            connect_to_known_node(node_url)"""

    app.run(host='0.0.0.0', port=8080, debug=True)