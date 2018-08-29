import pyqtgraph as pg
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from numpy import matrix
# Anser Import
import utils.utils as utils
import sys

class FFTGraph(QWidget):
    '''
    Represents the frequencies emitted by the field generator.
    A fast fourier transform is applied to the samples acquired from the data acquisition device.
    This is a useful debugging tool.
    '''
    def __init__(self):
        super(FFTGraph, self).__init__()
        pg.setConfigOption('background', 'w')
        pg.setConfigOption('foreground', 'k')
        self.graph = pg.PlotWidget()
        self.graph.plotItem.setTitle('Field Generator Frequencies')
        self.graph.plotItem.setLabel('bottom', 'Frequency (Hz)')
        self.graph.plotItem.setLabel('left', 'Magnitude')
        self.graph.curve = self.graph.plot(pen=pg.mkPen(color=(0, 0, 0), width=1.5))
        self.graph.setXRange(0, 4000, padding=-10)
        self.graph.setYRange(0, -120, padding=0)

        layout = QVBoxLayout()

        self.channelComboBox = QComboBox()
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.channelComboBox.setMinimumWidth(200)
        self.channelComboBox.setSizePolicy(sizePolicy)
        self.channelComboBox.currentIndexChanged.connect(self.channelChanged)

        self.setLayout(layout)
        layout.addWidget(self.graph)
        layout.addWidget(self.channelComboBox)
        self.channel = -1

    @pyqtSlot(int)
    def channelChanged(self, i):
        self.channel = i

    @pyqtSlot(object)
    def populateCombo(self, system):
        self.channelComboBox.clear()
        self.channelComboBox.addItem('Coil Sensing Channel', 0)
        for item in system.channels:
            self.channelComboBox.addItem('Channels {}'.format(str(item)), int(item))

    @pyqtSlot(matrix, float)
    def updateGraph(self, samples, sampling_freq):
        frequencies, magnitudes_in_db = utils.convert_samples_to_fft(samples, self.channel, sampling_freq)
        self.graph.curve.setData(frequencies, magnitudes_in_db)

    def clearGraph(self):
        self.graph.curve.clear()
