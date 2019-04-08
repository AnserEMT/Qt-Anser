""" Starts tracking and displays system information """
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import pyqtSignal, pyqtSlot
from app.gui.QtUI.systemwidget import Ui_systemwidget
import app.utilities.guiutils as guiutils


class SystemPanel(QWidget, Ui_systemwidget):
    """
    Allows the user to activate the EMT system and start tracking.
    User can select what sensors, ports and system speed to use.

    :param Ui_systemwidget: automatically generated python class from Qt Designer UI file *systemwidget.ui*
    """

    #: **(QtSignal) UI request:** to start tracking i.e. instantiate EMT system with the given list of sensors and tracking speed (1-4)
    UI_REQUEST_CREATE_SYSTEM = pyqtSignal(list, list, int)

    def __init__(self):
        super(SystemPanel, self).__init__()
        # Instantiates the TrackingPanel UI (Qt Designer UI file)
        self.setupUi(self)
        # apply_button - to start tracking and instantiate the system with the given list of sensors and tracking speed/
        self.apply_button.clicked.connect(lambda: self.UI_REQUEST_CREATE_SYSTEM.emit([self.combo_1.currentData(),
                                                                                      self.combo_2.currentData(),
                                                                                      self.combo_3.currentData(),
                                                                                      self.combo_4.currentData()],

                                                                                     [self.checkbox_1.isChecked(),
                                                                                      self.checkbox_2.isChecked(),
                                                                                      self.checkbox_3.isChecked(),
                                                                                      self.checkbox_4.isChecked()],
                                                                                     self.slider.value()))
        # Frequency Labels for each of the transmitter coils (kHz)
        self.coilFreqLabels = []
        self.coilFreqLabels.extend([self.coil_1f, self.coil_2f, self.coil_3f, self.coil_4f,
                                    self.coil_5f, self.coil_6f, self.coil_7f, self.coil_8f])

        # Status LEDs for each of the transmitter(ON=Green, OFF=Grey)
        self.coilLEDs = []
        self.coilLEDs.extend([self.coil_1, self.coil_2, self.coil_3, self.coil_4,
                              self.coil_5, self.coil_6, self.coil_7, self.coil_8])

        # Initially set LED status to OFF for each fo the transmitter coils
        self.setCoilLEDs([False] * 8)

        # Each combobox represents a port (1-4).
        # Each combobox contains all the calibrated sensors on that port.
        self.combos = [self.combo_1, self.combo_2, self.combo_3, self.combo_4]


    @pyqtSlot(object)
    def setSystemInfo(self, system):
        """ Sets the EMT System information in the side panel.
        e.g. sampling frequency, refresh rate, active ports, transmitter coil frequencies.
        Called once tracking begins.

        :param system: the system object describing current tracking settings
        """
        self.sampling_frequency.setText(str(system.sampling_freq))
        self.refresh_rate.setText(str(system.num_samples))
        self.active_ports.setText(str(system.active_ports))
        for index, freq in enumerate(system.freq):
            self.coilFreqLabels[index].setText(str(freq))
        self.setCoilLEDs(system.coils)


    @pyqtSlot(bool)
    def setAllCoilLEDs(self, status):
        """ Sets the LED status for each of the transmitter coils.

        :param status: a boolean describing the status of all coils
        """
        for LED in self.coilLEDs:
            LED.setPixmap(guiutils.get_status_pixmap(status))
            LED.setProperty('status', status)


    def setCoilLED(self, coilNr, status):
        """ Sets the LED status for a single transmitter coil.

        :param coilNr: the given coil (1-8)
        :param status: a boolean describing the status of the given coil
        """
        if status != self.coilLEDs[coilNr - 1].property('status'):
            self.coilLEDs[coilNr - 1].setPixmap(guiutils.get_status_pixmap(status))


    def setCoilLEDs(self, statusList):
        """ Sets the LED status for each of the transmitter coils using a boolean list.

        :param statusList: list of booleans describing the status of all coils (1-8)
        """
        for index, LED in enumerate(self.coilLEDs):
            LED.setPixmap(guiutils.get_status_pixmap(statusList[index]))


    def setCoilLEDsByID(self, statusIDList):
        """ Sets the LED status for each of the transmitter coils using a boolean dictionary."""
        for index, (statusID, LED) in enumerate(zip(statusIDList, self.coilLEDs)):
            LED.setPixmap(guiutils.get_status_pixmap_by_ID(statusID))


    @pyqtSlot(list)
    def populateCombos(self, sensors):
        """ Populate the combobox with all available sensors.

        :param sensors: the given list of sensors
        """
        for combo in self.combos:
            combo.clear()
        for sensor in sensors:
            for comboNo, combo in enumerate(self.combos):
                if comboNo+1 in sensor.ports:
                    combo.addItem(sensor.name, sensor.name)
