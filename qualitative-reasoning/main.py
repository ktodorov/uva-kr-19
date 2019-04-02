from node import Node
import utils

node1 = Node(1, 'darkblue', [2, 3])
node2 = Node(2, 'darkred', [3])
node3 = Node(3, 'darkgreen', [])

nodes = [node1, node2, node3]
utils.create_representation_graph(nodes, 'white', 1000)