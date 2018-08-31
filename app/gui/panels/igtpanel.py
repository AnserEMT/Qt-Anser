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

    def __init__(self):
        super(IGTPanel, self).__init__()
        self.setupUi(self)
        self.setStatus(False)
        self.apply_button.clicked.connect(lambda: self.UI_REQUEST_CREATE_SERVER.emit(self.port.text(),
                                                                                     self.localhost.isChecked()))

    def setIncomingBrowser(self, message):
        self.incoming_browser.clear()
        self.incoming_browser.setText(message)

    @pyqtSlot(bool)
    def setStatus(self, connected):
        self.status.setPixmap(guiutils.get_status_pixmap(connected))

    @pyqtSlot(list)
    def setCoordinates(self, positions):
        #TODO: this just works for one sensor
        self.x_label.setText(str(round(positions[0][0],2)))
        self.y_label.setText(str(round(positions[0][1],2)))
        self.z_label.setText(str(round(positions[0][2],2)))
