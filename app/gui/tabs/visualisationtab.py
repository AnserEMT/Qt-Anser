""" Visualises sensors positions and activates an OpenIGTLink connection """
from PyQt5.QtWidgets import QSplitter, QWidget, QVBoxLayout
from PyQt5.QtCore import Qt
from app.gui.graphs.positiongraph import PositionGraph
from app.gui.panels.igtpanel import IGTPanel


class VisualisationTab(QWidget):
    """
    Contains a *3D visualisation graph* to display sensor positions.
    Also has a *side panel* to activate an OpenIGTLink connection.
    """
    def __init__(self):
        super(VisualisationTab, self).__init__()
        # 3D visualisation graph
        self.positionGraph = PositionGraph()
        # side panel
        self.igtPanel = IGTPanel()
        tabLayout = QVBoxLayout()
        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(self.positionGraph)
        splitter.addWidget(self.igtPanel)
        tabLayout.addWidget(splitter)
        tabLayout.setContentsMargins(18,18, 10, 25)
        self.setLayout(tabLayout)
