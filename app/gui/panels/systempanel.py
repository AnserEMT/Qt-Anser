'''Starts tracking and displays system info'''
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import pyqtSignal, pyqtSlot
from app.gui.QtUI.systemwidget import Ui_systemwidget
import app.utilities.guiutils as guiutils


class SystemPanel(QWidget, Ui_systemwidget):
    '''
    Allows the user to activate the EMT system and start tracking.
    User can select what sensors, ports and system speed to use.
    '''
    UI_REQUEST_CREATE_SYSTEM = pyqtSignal(list, list, int)

    def __init__(self):
        super(SystemPanel, self).__init__()
        self.setupUi(self)
        self.apply_button.clicked.connect(lambda: self.UI_REQUEST_CREATE_SYSTEM.emit([self.combo_1.currentData(),
                                                                                      self.combo_2.currentData(),
                                                                                      self.combo_3.currentData(),
                                                                                      self.combo_4.currentData()],

                                                                                     [self.checkbox_1.isChecked(),
                                                                                      self.checkbox_2.isChecked(),
                                                                                      self.checkbox_3.isChecked(),
                                                                                      self.checkbox_4.isChecked()],

                                                                                     self.slider.value()))
        self.coilFreqLabels = []
        self.coilFreqLabels.extend([self.coil_1f, self.coil_2f, self.coil_3f, self.coil_4f,
                                    self.coil_5f, self.coil_6f, self.coil_7f, self.coil_8f])

        self.coilLEDs = []
        self.coilLEDs.extend([self.coil_1, self.coil_2, self.coil_3, self.coil_4,
                              self.coil_5, self.coil_6, self.coil_7, self.coil_8])

        self.setCoilLEDs([False] * 8)
        self.combos = [self.combo_1, self.combo_2, self.combo_3, self.combo_4]

    @pyqtSlot(object)
    def setSystemInfo(self, system):
        self.sampling_frequency.setText(str(system.sampling_freq))
        self.refresh_rate.setText(str(system.num_samples))
        self.active_ports.setText(str(system.active_ports))
        for index, freq in enumerate(system.freq):
            self.coilFreqLabels[index].setText(str(freq))
        self.setCoilLEDs(system.coils)

    @pyqtSlot(bool)
    def setAllCoilLEDs(self, status):
        for LED in self.coilLEDs:
            LED.setPixmap(guiutils.get_status_pixmap(status))
            LED.setProperty('status', status)

    def setCoilLED(self, coilNr, status):
        if status != self.coilLEDs[coilNr - 1].property('status'):
            self.coilLEDs[coilNr - 1].setPixmap(guiutils.get_status_pixmap(status))

    def setCoilLEDs(self, statusList):
        for index, LED in enumerate(self.coilLEDs):
            LED.setPixmap(guiutils.get_status_pixmap(statusList[index]))

    def setCoilLEDsByID(self, statusIDList):
        for index, (statusID, LED) in enumerate(zip(statusIDList, self.coilLEDs)):
            LED.setPixmap(guiutils.get_status_pixmap_by_ID(statusID))

    @pyqtSlot(list)
    def populateCombos(self, sensors):
        for combo in self.combos:
            combo.clear()
        for sensor in sensors:
            for comboNo, combo in enumerate(self.combos):
                if comboNo+1 in sensor.ports:
                    combo.addItem(sensor.name, sensor.name)
