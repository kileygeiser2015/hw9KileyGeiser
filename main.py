import os
os.environ["QT_OPENGL"] = "software"
os.environ["QT_ANGLE_PLATFORM"] = "d3d9"
os.environ["QT_QUICK_BACKEND"] = "software"

import sys
from PyQt5.QtWidgets import QApplication
from truss_gui import TrussViewer

if __name__ == '__main__':
    app = QApplication(sys.argv)
    viewer = TrussViewer()
    viewer.show()
    sys.exit(app.exec_())








