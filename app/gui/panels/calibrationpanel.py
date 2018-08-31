'''Starts calibration and creates/removes sensors'''
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import pyqtSignal, pyqtSlot
from app.gui.QtUI.calibrationwidget import Ui_calibrationwidget


class CalibrationPanel(QWidget, Ui_calibrationwidget):
    '''
    Allows the user to activate the system and start calibrating.
    User must select the appropriate sensor and port.
    '''
    UI_REQUEST_CREATE_NEW_SENSOR = pyqtSignal(str, str, str)
    UI_REQUEST_REMOVE_SENSOR = pyqtSignal(str)
    UI_REQUEST_CREATE_CALIBRATION_SYSTEM = pyqtSignal(str, int)
    UI_REQUEST_CAPTURE_POINT = pyqtSignal()
    UI_REQUEST_CALIBRATE = pyqtSignal()

    def __init__(self):
        super(CalibrationPanel, self).__init__()
        self.setupUi(self)
        self.add_button.clicked.connect(lambda: self.UI_REQUEST_CREATE_NEW_SENSOR.emit(self.name.text(),
                                                                                       self.description.text(),
                                                                                       self.dof_combobox.currentText()))
        self.remove_button.clicked.connect(lambda: self.UI_REQUEST_REMOVE_SENSOR.emit(self.sensor_combobox.currentText()))

        self.start_button.clicked.connect(lambda: self.UI_REQUEST_CREATE_CALIBRATION_SYSTEM.emit(self.cal_sensor_combobox.currentData(),
                                                                                                 int(self.port_combobox.currentText())))
        #join up these into one
        self.point_capture_button.clicked.connect(self.UI_REQUEST_CAPTURE_POINT.emit)
        self.point_capture_button.clicked.connect(self.capturing)

        #join up these into one
        self.calibrate_button.clicked.connect(self.UI_REQUEST_CALIBRATE.emit)
        self.calibrate_button.clicked.connect(self.calibrating)
        self.defaultSetup()

    @pyqtSlot(int)
    def setNextCapture(self, num):
        self.point_label.setText(str(num))
        self.status_label.setText('Ready')

    @pyqtSlot()
    def setReadyToCapture(self):
        self.status_label.setText('Ready to capture point')
        self.point_capture_button.setEnabled(True)
        self.point_capture_button.setAutoDefault(True)
        self.point_capture_button.setDefault(True)

    @pyqtSlot()
    def setReadyToCalibrate(self):
        self.point_label.setText('All Captured ')
        self.status_label.setText('Ready to Calibrate ')
        self.point_capture_button.setEnabled(False)
        self.calibrate_button.setEnabled(True)

    @pyqtSlot()
    def setCalibrationComplete(self):
        self.defaultSetup()

    def capturing(self):
        self.status_label.setText('Capturing ......')

    def calibrating(self):
        self.status_label.setText('Calibrating ......')

    def defaultSetup(self):
        self.status_label.setText('None')
        self.point_label.setText('None')
        self.calibrate_button.setEnabled(False)
        self.point_capture_button.setEnabled(False)

    @pyqtSlot(list)
    def populateCombosWithSensors(self, sensors):
        self.sensor_combobox.clear()
        self.cal_sensor_combobox.clear()
        for sensor in sensors:
            self.sensor_combobox.addItem(sensor.name, sensor.name)
            self.cal_sensor_combobox.addItem(sensor.name, sensor.name)

