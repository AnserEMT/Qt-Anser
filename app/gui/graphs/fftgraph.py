"""  Shows the frequencies emitted by the field generator in real time. """
import pyqtgraph as pg
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from numpy import matrix
# Anser Import
import utils.utils as utils
import sys

class FFTGraph(QWidget):
    """
    Represents the frequencies emitted by the field generator.
    A *fast fourier transform* is applied to the samples acquired from the data acquisition device.
    This is a useful debugging tool.
    """
    def __init__(self):
        super(FFTGraph, self).__init__()
        # change background colour of (FFT) plot graph
        pg.setConfigOption('background', 'w')
        pg.setConfigOption('foreground', 'k')
        # create a (FFT) plot graph and label axes
        self.graph = pg.PlotWidget()
        self.graph.plotItem.setTitle('Field Generator Frequencies')
        self.graph.plotItem.setLabel('bottom', 'Frequency (Hz)')
        self.graph.plotItem.setLabel('left', 'Magnitude')
        # create and stylise the curve for the (FFT) plot graph
        self.graph.curve = self.graph.plot(pen=pg.mkPen(color=(0, 0, 0), width=1.5))
        self.graph.setXRange(0, 4000, padding=-10)
        self.graph.setYRange(0, -120, padding=0)

        layout = QVBoxLayout()

        # create a combobox for all available sensor channels.
        self.channelComboBox = QComboBox()
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.channelComboBox.setMinimumWidth(200)
        self.channelComboBox.setSizePolicy(sizePolicy)

        # The FFT graph corresponds to a single sensor channel.
        # When the current sensor channel changes, the FFT will performed on the samples for that channel.
        self.channelComboBox.currentIndexChanged.connect(self.channelChanged)

        self.setLayout(layout)
        layout.addWidget(self.graph)
        layout.addWidget(self.channelComboBox)
        self.channel = -1

    @pyqtSlot(int)
    def channelChanged(self, i):
        """ Sets the index of the current sensor channel.
        Called when the user selects a new sensor channel from the channelCombobox.


        :param i: the index of the current sensor channel (1-16)
        """
        self.channel = i

    @pyqtSlot(object)
    def populateCombo(self, system):
        """ Populates the channelCombobox with all available sensor channels.

        :param system: the system object describing current tracking details
        """
        self.channelComboBox.clear()
        self.channelComboBox.addItem('Coil Sensing Channel', 0)
        for channel in system.active_channels:
            self.channelComboBox.addItem('Channels {}'.format(str(channel)), int(channel))

    @pyqtSlot(matrix, float)
    def updateGraph(self, samples, sampling_freq):
        """ Performs an fft on received samples and displays frequencies on the (FFT) plot graph.
        NOTE: the FFT corresponds to a single sensor channel.

        :param samples: received samples from the EMT system
        :param sampling_freq: the given sampling frequency of the EMT system (e.g. 100000 hz)
        """
        frequencies, magnitudes_in_db = utils.convert_samples_to_fft(samples, self.channel, sampling_freq)
        self.graph.curve.setData(frequencies, magnitudes_in_db)

    def clearGraph(self):
        """ clears the (FFT) plot graph """
        self.graph.curve.clear()
