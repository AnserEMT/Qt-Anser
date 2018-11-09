'''Creates an OpenIGTLink server'''
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import pyqtSlot, pyqtSignal
from app.gui.QtUI.igtwidget import Ui_igtwidget
import app.utilities.guiutils as guiutils


class IGTPanel(QWidget, Ui_igtwidget):
    '''
    Allows the user to create a server and transfer sensor positions via OpenIGTLink.
    '''
    UI_REQUEST_CREATE_SERVER = pyqtSignal(str, bool)
    UI_REQUEST_RESET_POSITION = pyqtSignal()

    def __init__(self):
        super(IGTPanel, self).__init__()
        self.setupUi(self)
        self.setStatus(False)
        self.apply_button.clicked.connect(lambda: self.UI_REQUEST_CREATE_SERVER.emit(self.port.text(),
                                                                                     self.localhost.isChecked()))
        self.reset_position_button.clicked.connect(lambda: self.UI_REQUEST_RESET_POSITION.emit())

    def setIncomingBrowser(self, message):
        self.incoming_browser.clear()
        self.incoming_browser.setText(message)

    @pyqtSlot(bool)
    def setStatus(self, connected):
        self.status.setPixmap(guiutils.get_status_pixmap(connected))

    def populateCombo(self, system):
        self.sensor_combo.clear()
        for index, sensor in enumerate(system.sensors):
            self.sensor_combo.addItem(str(sensor.name), index)


    @pyqtSlot(list)
    def setCoordinates(self, positions):
        index = int(self.sensor_combo.currentData())
        self.x_label.setText(str(round(positions[index][0],2)))
        self.y_label.setText(str(round(positions[index][1],2)))
        self.z_label.setText(str(round(positions[index][2],2)))
