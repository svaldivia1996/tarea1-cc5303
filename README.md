# tarea1-cc5303
## Para la ejecucion usando docker compose
`docker-compose up -d`


## Para ejecucion usando solo Dockerfile
Primero crear una network para los contenedores
`docker network create mynetwork`

Hacer la imagen de app.py
`docker build -t my-flask-app .`

Luego crear los containers que son nuestros nodos
Para caso de uso crear 4 nodos
#### Ejemplo de nodo 1
    `docker run -d -p 8081:8080 -e PORT=8081 --name nodo1 --network=mynetwork my-flask-app`
#### Ejemplo de nodo 2
    `docker run -d -p 8082:8080 -e PORT=8082 --name nodo2 --network=mynetwork my-flask-app`
#### Ejemplo de nodo 3
    `docker run -d -p 8083:8080 -e PORT=8083 --name nodo3 --network=mynetwork my-flask-app`
#### Ejemplo de nodo 4
    `docker run -d -p 8084:8080 -e PORT=8084 --name nodo4 --network=mynetwork my-flask-app`

## Para uso

Luego para revisar los nodos vecinos por ejemplo del nodo 1, en un inicio solo se conocen a si mismos:
http://localhost:8081/nodes

Un ejemplo de peticion POST para conectar el nodo 1 cuya ip es  (172.193.0.5 con puerto 8081) al nodo 3:
`curl -X POST -H "Content-Type: application/json" -d '{"node_address": "172.19.0.5", "node_port": "8081"}' http://localhost:8083/connect `

finalmente revisar en
    -http://localhost:8081/nodes
    -http://localhost:8083/nodes
para verificar si fueron conectados.
