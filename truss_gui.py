import math
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QGraphicsView, QGraphicsScene, QPushButton,
    QDoubleSpinBox, QFileDialog, QGraphicsLineItem, QLabel, QGroupBox,
    QHBoxLayout, QTextEdit, QLineEdit, QGridLayout
)
from PyQt5.QtGui import QPen, QColor, QPixmap, QPainter
from PyQt5.QtCore import Qt, QPointF
from truss_model import parse_truss_file, get_longest_link, draw_truss


class TrussViewer(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Truss Visualizer")
        self.resize(1200, 800)

        # Layout
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Controls
        self.controls = QHBoxLayout()
        self.btn_load = QPushButton("Open Truss File")
        self.btn_load.clicked.connect(self.load_truss_file)
        self.controls.addWidget(self.btn_load)

        self.controls.addWidget(QLabel("Zoom"))
        self.zoom_spinner = QDoubleSpinBox()
        self.zoom_spinner.setRange(0.1, 10.0)
        self.zoom_spinner.setValue(1.0)
        self.zoom_spinner.valueChanged.connect(self.set_zoom)
        self.controls.addWidget(self.zoom_spinner)

        self.btn_export = QPushButton("Export Image")
        self.btn_export.clicked.connect(self.export_image)
        self.controls.addWidget(self.btn_export)

        self.layout.addLayout(self.controls)

        # Graphics view
        self.view = QGraphicsView()
        self.scene = QGraphicsScene()
        self.view.setScene(self.scene)
        self.layout.addWidget(self.view)

        # Report box
        self.report_box = QTextEdit()
        self.report_box.setReadOnly(True)
        self.layout.addWidget(self.report_box)

        # Longest link box
        self.link_info_group = QGroupBox("Longest Link")
        self.link_layout = QGridLayout()
        self.link_name = QLineEdit(); self.link_name.setReadOnly(True)
        self.node1_name = QLineEdit(); self.node1_name.setReadOnly(True)
        self.node2_name = QLineEdit(); self.node2_name.setReadOnly(True)
        self.link_length = QLineEdit(); self.link_length.setReadOnly(True)

        self.link_layout.addWidget(QLabel("Link Name:"), 0, 0)
        self.link_layout.addWidget(self.link_name, 0, 1)
        self.link_layout.addWidget(QLabel("Node 1:"), 1, 0)
        self.link_layout.addWidget(self.node1_name, 1, 1)
        self.link_layout.addWidget(QLabel("Node 2:"), 2, 0)
        self.link_layout.addWidget(self.node2_name, 2, 1)
        self.link_layout.addWidget(QLabel("Length:"), 3, 0)
        self.link_layout.addWidget(self.link_length, 3, 1)

        self.link_info_group.setLayout(self.link_layout)
        self.layout.addWidget(self.link_info_group)

    def set_zoom(self):
        self.view.resetTransform()
        self.view.scale(self.zoom_spinner.value(), self.zoom_spinner.value())

    def load_truss_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open Truss File", "", "Text Files (*.txt *.csv)")
        if not file_path:
            return

        self.scene.clear()
        self.report_box.clear()

        nodes, links, reactions = parse_truss_file(file_path)

        draw_truss(self.scene, nodes, links, reactions)

        for name, point in nodes.items():
            self.report_box.append(f"Node: {name} at ({point.x():.1f}, {-point.y():.1f})")
        for link in links:
            self.report_box.append(f"Link: {link[0]} between {link[1]} and {link[2]}")
        for support, loc in reactions:
            self.report_box.append(f"Support at {support} with reaction at ({loc.x():.1f}, {-loc.y():.1f})")

        longest = get_longest_link(nodes, links)
        if longest:
            self.link_name.setText(longest[0])
            self.node1_name.setText(longest[1])
            self.node2_name.setText(longest[2])
            self.link_length.setText(f"{longest[3]:.2f}")

    def export_image(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Export Image", "truss_diagram.png", "PNG Files (*.png)")
        if not file_path:
            return
        rect = self.scene.sceneRect()
        image = QPixmap(int(rect.width()), int(rect.height()))
        image.fill(Qt.white)
        painter = QPainter(image)
        self.scene.render(painter)
        painter.end()
        image.save(file_path, "PNG")
