""" Creates an OpenIGTLink server """
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import pyqtSlot, pyqtSignal
from app.gui.QtUI.igtwidget import Ui_igtwidget
import app.utilities.guiutils as guiutils
import utils.utils as utils

class IGTPanel(QWidget, Ui_igtwidget):
    """
    Allows the user to create a server and transfer sensor positions to client applications/devices via OpenIGTLink.

    :param Ui_igtwidget: automatically generated python class from Qt Designer UI file *igtwidget.ui*
    """

    #: **(QtSignal) UI request:** to host an OpenIGTLink connection.
    UI_REQUEST_CREATE_SERVER = pyqtSignal(str, bool)
    #: **(QtSignal) UI request:** to reset sensor positions (solver can get stuck, this is a temporary solution)
    UI_REQUEST_RESET_POSITION = pyqtSignal()

    def __init__(self):
        super(IGTPanel, self).__init__()
        # Instantiates the IGTPanel UI (Qt Designer UI file)
        self.setupUi(self)
        self.setStatus(False)
        self.tracking_volume = []

        # Creates an openIGTLink connection
        self.apply_button.clicked.connect(lambda: self.UI_REQUEST_CREATE_SERVER.emit(self.port.text(),
                                                                                     self.localhost.isChecked()))

        # reset sensor positions (as solver can get stuck )
        self.reset_position_button.clicked.connect(lambda: self.UI_REQUEST_RESET_POSITION.emit())

    @pyqtSlot(object)
    def setIGTInfo(self, system):
        """ Populates IGT panel using system object

        :param system: system object
        """
        self.tracking_volume = system.tracking_volume
        self.volume_label.setText(str('{}  x  {}  x  {} ').format(
            int(self.tracking_volume[0]), int(self.tracking_volume[1]), int(self.tracking_volume[2])))
        self.populateCombo(system)

    def setIncomingBrowser(self, message):
        """ Displays the given message in the side panel. Used for displaying incoming OpenIGTLink messages.

        :param message: the given message
        """
        self.incoming_browser.clear()
        self.incoming_browser.setText(message)

    @pyqtSlot(bool)
    def setStatus(self, connected):
        """ Sets the LED status for the OpenIGTLink connection. (ON=Green, OFF=Grey)

        :param connected: a boolean describing the status of the
        """
        self.status.setPixmap(guiutils.get_status_pixmap(connected))

    def populateCombo(self, system):
        """ Populates the sensor_combobox with all the available sensor files

        :param system: the system object describing current tracking settings
        """
        self.sensor_combo.clear()
        for index, sensor in enumerate(system.sensors):
            self.sensor_combo.addItem(str(sensor.name), index)

    @pyqtSlot(list)
    def setCoordinates(self, positions):
        """ Shows the coordinates (X,Y,Z) for the currently selected sensor

        :param positions: list of sensor positions
        """
        index = int(self.sensor_combo.currentData())
        self.x_label.setText(str(round(positions[index][0],2)))
        self.y_label.setText(str(round(positions[index][1],2)))
        self.z_label.setText(str(round(positions[index][2],2)))

        bounds = utils.is_position_in_tracking_volume(positions[index], self.tracking_volume)
        self.bounds_label.setText("IN") if bounds is True else self.bounds_label.setText("OUT")

    @pyqtSlot(bool)
    def resetPanel(self):
        """ Resets the IGT Panel and LEDs"""
        self.incoming_browser.clear()
        self.sensor_combo.clear()
        self.x_label.setText('0')
        self.y_label.setText('0')
        self.z_label.setText('0')