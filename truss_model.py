import math
from PyQt5.QtCore import QPointF


class Link:
    def __init__(self, name, node1, node2, width, thickness, material):
        self.name = name
        self.node1 = node1
        self.node2 = node2
        self.width = width
        self.thickness = thickness
        self.material = material
        self.length = 0.0
        self.weight = 0.0

    def compute_geometry(self, nodes):
        if self.node1 in nodes and self.node2 in nodes:
            p1 = nodes[self.node1]
            p2 = nodes[self.node2]
            self.length = math.hypot(p2.x() - p1.x(), p2.y() - p1.y())

            # Assume density of material (e.g., steel or aluminum)
            density = 7850 if self.material.lower() == "steel" else 2700
            volume = self.width * self.thickness * self.length
            self.weight = density * volume  # in kg·mm^2 (adjust units if needed)


def parse_truss_file(file_path):
    nodes = {}
    links = []
    reactions = {}

    with open(file_path, 'r') as f:
        lines = f.readlines()

    for line in lines:
        tokens = [t.strip() for t in line.split(',')]
        if not tokens or len(tokens) < 2:
            continue

        if tokens[0].lower() == "node":
            name, x, y = tokens[1], float(tokens[2]), float(tokens[3])
            nodes[name] = QPointF(x, -y)  # Flip y for display

        elif tokens[0].lower() == "link":
            name = tokens[1]
            n1 = tokens[2]
            n2 = tokens[3]
            width = float(tokens[4])
            thickness = float(tokens[5])
            material = tokens[6]
            link = Link(name, n1, n2, width, thickness, material)
            link.compute_geometry(nodes)
            links.append(link)

    return nodes, links, reactions
from PyQt5.QtWidgets import QGraphicsLineItem
from PyQt5.QtGui import QPen
from PyQt5.QtCore import Qt

def get_longest_link(links):
    if not links:
        return None
    return max(links, key=lambda l: l.length)


def draw_truss(scene, nodes, links):
    scene.clear()
    pen = QPen(Qt.black)
    pen.setWidth(2)

    for link in links:
        if link.node1 in nodes and link.node2 in nodes:
            p1 = nodes[link.node1]
            p2 = nodes[link.node2]
            line = QGraphicsLineItem(p1.x(), p1.y(), p2.x(), p2.y())
            line.setPen(pen)
            scene.addItem(line)



