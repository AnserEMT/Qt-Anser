""" Starts tracking and displays EMT system information """
from PyQt5.QtWidgets import QWidget, QSplitter, QVBoxLayout
from PyQt5.QtCore import Qt
from app.gui.graphs.fftgraph import FFTGraph
from app.gui.panels.systempanel import SystemPanel


class SystemTab(QWidget):
    """
    Contains a fast fourier transform *(FFT) graph* showing the frequencies emitted by the field generator.
    Also has a *side panel* to start tracking and display EMT system information.
    """
    def __init__(self):
        super(SystemTab, self).__init__()
        # FFT graph
        self.fftGraph = FFTGraph()
        # side panel
        self.systemPanel = SystemPanel()
        tabLayout = QVBoxLayout()
        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(self.fftGraph)
        splitter.addWidget(self.systemPanel)
        tabLayout.addWidget(splitter)
        self.setLayout(tabLayout)







