""" Starts the calibration procedure and creates/removes sensor files """
from PyQt5.QtWidgets import QSplitter, QWidget, QVBoxLayout
from PyQt5.QtCore import Qt
from app.gui.panels.calibrationpanel import CalibrationPanel
from app.gui.graphs.gridgraph import GridGraph


class CalibrationTab(QWidget):
    """
    Contains a graph representing the EMT transmitter board with a *grid of calibration test points*.
    Also has a *side panel* to allow the user to start the calibration procedure and create/remove sensor files.
    """
    def __init__(self):
        super(CalibrationTab, self).__init__()
        # grid of calibration test points
        self.gridwidget = GridGraph()
        # side panel
        self.calibrationPanel = CalibrationPanel()
        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(self.gridwidget)
        splitter.addWidget(self.calibrationPanel)
        tabLayout = QVBoxLayout()
        tabLayout.addWidget(splitter)
        self.setLayout(tabLayout)
