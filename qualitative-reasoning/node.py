from typing import List


class Node:
    def __init__(self, label: any, color: str, connections: List[str] = []):
        self.label = label
        self.color = color
        self.connections = connections

    def add_connections(self, connections):
        self.connections.extend(connections)