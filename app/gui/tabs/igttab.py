from PyQt5.QtWidgets import QSplitter, QWidget, QVBoxLayout
from PyQt5.QtCore import Qt
from app.gui.graphs.positiongraph import PositionGraph
from app.gui.panels.igtpanel import IGTPanel


class IGTTab(QWidget):
    '''
    Contains a 3D visualisation view to display sensor positions and a side panel to activate OpenIGTLink.
    '''
    def __init__(self):
        super(IGTTab, self).__init__()
        self.positionGraph = PositionGraph()
        self.igtPanel = IGTPanel()
        tabLayout = QVBoxLayout()
        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(self.positionGraph)
        splitter.addWidget(self.igtPanel)
        tabLayout.addWidget(splitter)
        tabLayout.setContentsMargins(18,18, 10, 25)
        self.setLayout(tabLayout)
