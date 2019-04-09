""" Connects the UI to the Anser system """
from PyQt5.QtCore import Qt, pyqtSlot, QObject

class MainController(QObject):
    """ The controller is responsible for the control flow of the application.
        It acts as the glue of the application by connecting the GUI to the Anser (EMT) system.
        It delegates UI events to the appropriate Anser (EMT) function, vice versa.
        It is based on the Observer Design Pattern (QT Signals and Slots).
    """
    def __init__(self, view, system):
        """
        :param view: :mod:`~app.mainwindow` instance (representing the UI)
        :param system: :mod:`~app.qtanser` instance (representing the Anser System)
        """
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

        '''----------------------------------------------------------------------------'''
        '''         Connect SYSTEM EVENTS (Subjects) to UI ELEMENTS (Observers)        '''
        '''----------------------------------------------------------------------------'''

        # (QtSignal) System Event: EMT mode changed
        self.system.SYS_EVENT_MODE_CHANGED.connect(self.view.setStatusbarMode)

        # (QtSignal) System Event: Starting Tracking Mode
        self.system.SYS_EVENT_MODE_TRACKING.connect(self.systemPanel.setSystemInfo)
        self.system.SYS_EVENT_MODE_TRACKING.connect(self.fftGraph.populateCombo)
        self.system.SYS_EVENT_MODE_TRACKING.connect(self.igtPanel.populateCombo)

        # (QtSignal) System Event: EMT System Status
        self.system.SYS_EVENT_SYSTEM_STATUS.connect(self.view.setStatusbarSystemLED)
        self.system.SYS_EVENT_SYSTEM_STATUS.connect(self.systemPanel.setAllCoilLEDs)
        self.system.SYS_EVENT_SYSTEM_STATUS.connect(self.fftGraph.clearGraph)
        self.system.SYS_EVENT_SYSTEM_STATUS.connect(self.positionGraph.clearGraph)
        self.system.SYS_EVENT_SYSTEM_STATUS.connect(self.igtPanel.incoming_browser.clear)
        self.system.SYS_EVENT_SYSTEM_STATUS.connect(self.calibrationPanel.setCalibrationComplete)
        self.system.SYS_EVENT_SYSTEM_STATUS.connect(self.gridGraph.resetGraph)

        # (QtSignal) System Event: OpenIGTLink Status
        self.system.SYS_EVENT_SERVER_STATUS.connect(self.igtPanel.setStatus)
        self.system.SYS_EVENT_SERVER_STATUS.connect(self.view.setStatusbarServerLED)

        # (QtSignal) System Event: Sensor files have changed
        self.system.SYS_EVENT_SENSORS_CHANGED.connect(self.calibrationPanel.populateCombosWithSensors)
        self.system.SYS_EVENT_SENSORS_CHANGED.connect(self.systemPanel.populateCombos)

        # (QtSignal) System Event: New positions acquired
        self.system.SYS_EVENT_POSITIONS_ACQUIRED.connect(self.positionGraph.updateGraph)
        self.system.SYS_EVENT_POSITIONS_ACQUIRED.connect(self.igtPanel.setCoordinates)

        # (QtSignal) System Event: New samples acquired
        self.system.SYS_EVENT_SAMPLES_ACQUIRED.connect(self.fftGraph.updateGraph)

        # (QtSignal) System Event: Incoming OpenIGTLink Message received
        self.system.SYS_EVENT_NETWORK_MSG_RECEIVED.connect(self.igtPanel.setIncomingBrowser)

        # (QtSignal) System Event: EMT System Monitor Notification
        self.system.SYS_EVENT_SYSTEM_STATUS_NOTIFICATION.connect(self.view.notificationHanlder)

        # (QtSignal) System Event: Calibration Events
        self.system.SYS_EVENT_MODE_CALIBRATION.connect(self.calibrationPanel.setReadyToCapture)
        self.system.SYS_EVENT_POINT_CAPTURED.connect(self.gridGraph.moveToPosition)
        self.system.SYS_EVENT_POINT_CAPTURED.connect(self.calibrationPanel.setNextCapture)
        self.system.SYS_EVENT_READY_TO_CALIBRATE.connect(self.calibrationPanel.setReadyToCalibrate)

        # thread calling controller.stopCalibration() others should connect to system status resert

        self.system.SYS_EVENT_CALIBRATION_COMPLETED.connect(self.system.stopCalibration)
        # self.controller.SYS_EVENT_MODE_CALIBRATION.connect(self.statusBarModeLabel)

        '''----------------------------------------------------------------------------'''
        '''       Connect UI ELEMENTS (Subjects) to SYSTEM FUNCTIONS (Observers)       '''
        '''----------------------------------------------------------------------------'''

        # (QtSignal) UI Request: start EMT tracking system and begin tracking
        self.systemPanel.UI_REQUEST_CREATE_SYSTEM.connect(
            self.system.startTracking)  # ->SYS_EVENT_SYSTEM_INITIALISED

        # (QtSignal) UI Request: start an OpenIGTLink Server
        self.igtPanel.UI_REQUEST_CREATE_SERVER.connect(self.system.startServer)

        # (QtSignal) UI Request: create/remove a sensor file
        self.calibrationPanel.UI_REQUEST_CREATE_NEW_SENSOR.connect(self.system.createNewSensor)
        self.calibrationPanel.UI_REQUEST_REMOVE_SENSOR.connect(self.system.removeSensor)
        self.system.SYS_EVENT_SENSORS_CHANGED.emit(self.system.getSensors())

        # (QtSignal) UI Request: start EMT tracking system and begin calibration
        self.calibrationPanel.UI_REQUEST_CREATE_CALIBRATION_SYSTEM.connect(self.system.startCalibration)
        self.calibrationPanel.UI_REQUEST_CAPTURE_POINT.connect(self.system.capturePoint)
        self.calibrationPanel.UI_REQUEST_CALIBRATE.connect(self.gridGraph.flash)
        self.calibrationPanel.UI_REQUEST_CALIBRATE.connect(self.system.calibrate)

        # (QtSignal) UI Request: change default configuration file
        self.configEditor.UI_REQUEST_CHANGE_DEFAULT_CONFIG.connect(self.view.changeDefaultConfig)
        self.igtPanel.UI_REQUEST_RESET_POSITION.connect(self.system.resetPositions)
