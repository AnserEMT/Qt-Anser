""" Starts the calibration procedure and creates/removes sensor files """
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import pyqtSignal, pyqtSlot
from app.gui.QtUI.calibrationwidget import Ui_calibrationwidget


class CalibrationPanel(QWidget, Ui_calibrationwidget):
    """
    Allows the user to start the calibration procedure. User must select the appropriate sensor and port it is connected to.
    Also, allows the user to creates/removes sensor files.

    :param Ui_calibrationwidget: automatically generated python class from Qt Designer UI file *calibrationwidget.ui*
    """

    #: **(QtSignal) UI request:** to create a new sensor
    UI_REQUEST_CREATE_NEW_SENSOR = pyqtSignal(str, str, str)
    #: **(QtSignal) UI request:** to remove the given sensor
    UI_REQUEST_REMOVE_SENSOR = pyqtSignal(str)
    #: **(QtSignal) UI request:** to start calibrating the system with the given sensor (on the given port)
    UI_REQUEST_CREATE_CALIBRATION_SYSTEM = pyqtSignal(str, int)
    #: **(QtSignal) UI request:** to capture the next point
    UI_REQUEST_CAPTURE_POINT = pyqtSignal()
    #: **(QtSignal) UI request:** to calibrate the system (called once all points have been captured)
    UI_REQUEST_CALIBRATE = pyqtSignal()

    def __init__(self):
        super(CalibrationPanel, self).__init__()
        # Instantiates the CalibrationPanel UI (Qt Designer UI file)
        self.setupUi(self)
        # Creates a new sensor file
        self.add_button.clicked.connect(lambda: self.UI_REQUEST_CREATE_NEW_SENSOR.emit(self.name.text(),
                                                                                       self.description.text(),
                                                                                       self.dof_combobox.currentText()))
        # Removes the currently selected sensor file
        self.remove_button.clicked.connect(lambda: self.UI_REQUEST_REMOVE_SENSOR.emit(self.sensor_combobox.currentText()))

        # Starts the calibration procedure
        self.start_button.clicked.connect(lambda: self.UI_REQUEST_CREATE_CALIBRATION_SYSTEM.emit(self.cal_sensor_combobox.currentData(),
                                                                                                 int(self.port_combobox.currentText())))
        # TODO: join up these into one
        self.point_capture_button.clicked.connect(self.UI_REQUEST_CAPTURE_POINT.emit)
        self.point_capture_button.clicked.connect(self.capturing)

        # TODO: join up these into one
        self.calibrate_button.clicked.connect(self.UI_REQUEST_CALIBRATE.emit)
        self.calibrate_button.clicked.connect(self.calibrating)
        self.defaultSetup()

    @pyqtSlot(int)
    def setNextCapture(self, num):
        """ Indicates the next test point to be captured.
        Called after capturing each test point. """
        self.point_label.setText(str(num))
        self.status_label.setText('Ready')

    @pyqtSlot()
    def setReadyToCapture(self):
        """Called once the calibration procedure has begun"""
        self.status_label.setText('Ready to capture point')
        self.point_capture_button.setEnabled(True)
        self.point_capture_button.setAutoDefault(True)
        self.point_capture_button.setDefault(True)

    @pyqtSlot()
    def setReadyToCalibrate(self):
        """Called once all points have been capture"""
        self.point_label.setText('All Captured ')
        self.status_label.setText('Ready to Calibrate ')
        self.point_capture_button.setEnabled(False)
        self.calibrate_button.setEnabled(True)

    @pyqtSlot()
    def setCalibrationComplete(self):
        """ Default setup for the calibration procedure.
        Called at the end of the calibration procedure.
        """
        self.defaultSetup()

    def capturing(self):
        """ Sets the status label to 'Capturing'"""
        self.status_label.setText('Capturing ......')

    def calibrating(self):
        """ Sets the status label to 'calibrating'"""
        self.status_label.setText('Calibrating ......')

    def defaultSetup(self):
        """ Resets labels and re-enables buttons at the end of the calibration procedure"""
        self.status_label.setText('None')
        self.point_label.setText('None')
        self.calibrate_button.setEnabled(False)
        self.point_capture_button.setEnabled(False)

    @pyqtSlot(list)
    def populateCombosWithSensors(self, sensors):
        """ Populates the sensor_combobox with all available sensors

        :param sensors: given list of sensors
        """
        self.sensor_combobox.clear()
        self.cal_sensor_combobox.clear()
        for sensor in sensors:
            self.sensor_combobox.addItem(sensor.name, sensor.name)
            self.cal_sensor_combobox.addItem(sensor.name, sensor.name)

