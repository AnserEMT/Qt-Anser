'''Starts calibration and creates/removes sensors'''
from PyQt5.QtWidgets import QSplitter, QWidget, QVBoxLayout
from PyQt5.QtCore import Qt
from app.gui.panels.calibrationpanel import CalibrationPanel
from app.gui.graphs.gridgraph import GridGraph


class CalibrationTab(QWidget):
    '''Contains a grid of points representing the field generator board and a side panel'''
    def __init__(self):
        super(CalibrationTab, self).__init__()
        self.calibrationPanel = CalibrationPanel()
        self.gridwidget = GridGraph()
        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(self.gridwidget)
        splitter.addWidget(self.calibrationPanel)
        tabLayout = QVBoxLayout()
        tabLayout.addWidget(splitter)
        self.setLayout(tabLayout)
