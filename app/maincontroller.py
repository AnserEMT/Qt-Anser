from PyQt5.QtCore import Qt, pyqtSlot, QObject


class MainController(QObject):
    ''' The controller for the application, responsible for connecting the GUI and the EMT system. (View<->System)'''
    def __init__(self, view, system):
        super(MainController, self).__init__()
        self.view = view
        self.system = system

        self.systemPanel = self.view.tb.systemtab.systemPanel
        self.fftGraph = self.view.tb.systemtab.fftGraph
        self.positionGraph = self.view.tb.igttab.positionGraph
        self.igtPanel = self.view.tb.igttab.igtPanel
        self.calibrationPanel = self.view.tb.calibrationtab.calibrationPanel
        self.gridGraph = self.view.tb.calibrationtab.gridwidget.graph
        self.configEditor = self.view.tb.developertab

        # SYSTEM EVENTS
        self.system.SYS_EVENT_MODE_CHANGED.connect(self.view.setStatusBarMode)
        self.system.SYS_EVENT_MODE_TRACKING.connect(self.systemPanel.setSystemInfo)
        self.system.SYS_EVENT_MODE_TRACKING.connect(self.fftGraph.populateCombo)

        self.system.SYS_EVENT_SYSTEM_STATUS.connect(self.view.setStatusBarSystemLED)
        self.system.SYS_EVENT_SYSTEM_STATUS.connect(self.systemPanel.setAllCoilLEDs)
        self.system.SYS_EVENT_SYSTEM_STATUS.connect(self.fftGraph.clearGraph)
        self.system.SYS_EVENT_SYSTEM_STATUS.connect(self.positionGraph.clearGraph)
        self.system.SYS_EVENT_SYSTEM_STATUS.connect(self.igtPanel.incoming_browser.clear)
        self.system.SYS_EVENT_SYSTEM_STATUS.connect(self.calibrationPanel.setCalibrationComplete)
        self.system.SYS_EVENT_SYSTEM_STATUS.connect(self.gridGraph.resetGraph)

        self.system.SYS_EVENT_SERVER_STATUS.connect(self.igtPanel.setStatus)
        self.system.SYS_EVENT_SERVER_STATUS.connect(self.view.setStatusBarLED)

        self.system.SYS_EVENT_SENSORS_CHANGED.connect(self.calibrationPanel.populateCombosWithSensors)
        self.system.SYS_EVENT_SENSORS_CHANGED.connect(self.systemPanel.populateCombos)

        self.system.SYS_EVENT_POSITIONS_ACQUIRED.connect(self.positionGraph.updateGraph)
        self.system.SYS_EVENT_POSITIONS_ACQUIRED.connect(self.igtPanel.setCoordinates)
        self.system.SYS_EVENT_SAMPLES_ACQUIRED.connect(self.fftGraph.updateGraph)

        self.system.SYS_EVENT_NETWORK_MSG_RECEIVED.connect(self.igtPanel.setIncomingBrowser)
        self.system.SYS_EVENT_SYSTEM_STATUS_NOTIFICATION.connect(self.view.notificationHanlder)

        self.system.SYS_EVENT_MODE_CALIBRATION.connect(self.calibrationPanel.setReadyToCapture)
        self.system.SYS_EVENT_POINT_CAPTURED.connect(self.gridGraph.moveToPosition)
        self.system.SYS_EVENT_POINT_CAPTURED.connect(self.calibrationPanel.setNextCapture)
        self.system.SYS_EVENT_READY_TO_CALIBRATE.connect(self.calibrationPanel.setReadyToCalibrate)

        # thread calling controller.stopCalibration() others should connect to system status resert

        self.system.SYS_EVENT_CALIBRATION_COMPLETED.connect(self.system.stopCalibration)
        # self.controller.SYS_EVENT_MODE_CALIBRATION.connect(self.statusBarModeLabel)

        # UI REQUESTS
        self.systemPanel.UI_REQUEST_CREATE_SYSTEM.connect(
            self.system.startTracking)  # ->SYS_EVENT_SYSTEM_INITIALISED
        self.igtPanel.UI_REQUEST_CREATE_SERVER.connect(self.system.startServer)
        self.calibrationPanel.UI_REQUEST_CREATE_NEW_SENSOR.connect(self.system.createNewSensor)
        self.calibrationPanel.UI_REQUEST_REMOVE_SENSOR.connect(self.system.removeSensor)
        self.calibrationPanel.UI_REQUEST_CREATE_CALIBRATION_SYSTEM.connect(self.system.startCalibration)
        self.calibrationPanel.UI_REQUEST_CAPTURE_POINT.connect(self.system.capturePoint)
        self.calibrationPanel.UI_REQUEST_CALIBRATE.connect(self.gridGraph.flash)
        self.calibrationPanel.UI_REQUEST_CALIBRATE.connect(self.system.calibrate)

        self.system.SYS_EVENT_SENSORS_CHANGED.emit(self.system.getSensors())
        self.configEditor.UI_REQUEST_CHANGE_DEFAULT_CONFIG.connect(self.view.changeDefaultConfig)
