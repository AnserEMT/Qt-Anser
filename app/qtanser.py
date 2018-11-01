'''Qt Interface for the Anser system'''
from pyqtgraph.Qt import QtCore
from PyQt5.QtCore import pyqtSignal,QObject, pyqtSlot
from rx.concurrency import QtScheduler
from rx.concurrency import NewThreadScheduler
import logging
from scipy import matrix
from collections import namedtuple
from app.calibrationthread import CalibrationThread
import app.utilities.guiutils as guiutils
# Anser Imports
from emtracker import EMTracker
from emcalibration import EMCalibration
from monitor.monitor import Monitor, SystemStatusNotification
import utils.utils as utils
from sensor.sensor import Sensor


MODE_IDLE = 'IDLE'
MODE_TRACKING = 'TRK'
MODE_CALIBRATING = 'CAL'


class QtAnser(QObject):
    ''' Allows the application to speak with the Anser(EMT) system.
    It encapsulates the `Emtracker` class in a `QObject` making it possible to invoke Anser(EMT) functions.
    Also, emits system events and data which is then consumed by the application
    e.g. Status info, samples, sensor positions and network messages.
    '''
    SYS_EVENT_MODE_CALIBRATION = pyqtSignal()
    SYS_EVENT_MODE_CHANGED = pyqtSignal(str)
    SYS_EVENT_MODE_TRACKING = pyqtSignal(object)

    SYS_EVENT_SYSTEM_STATUS = pyqtSignal(bool)
    SYS_EVENT_SYSTEM_STATUS_NOTIFICATION = pyqtSignal(object)

    SYS_EVENT_SERVER_STATUS = pyqtSignal(bool)
    SYS_EVENT_SENSORS_CHANGED = pyqtSignal(list)
    SYS_EVENT_POSITIONS_ACQUIRED = pyqtSignal(list)
    SYS_EVENT_SAMPLES_ACQUIRED = pyqtSignal(matrix, float)
    SYS_EVENT_FFT_ACQUIRED = pyqtSignal(list, list)
    SYS_EVENT_NETWORK_MSG_RECEIVED = pyqtSignal(str)

    SYS_EVENT_POINT_CAPTURED = pyqtSignal(int)
    SYS_EVENT_READY_TO_CALIBRATE = pyqtSignal()
    SYS_EVENT_CALIBRATION_COMPLETED = pyqtSignal()

    def __init__(self):
        super(QtAnser, self).__init__()
        self.anser = None
        self.calibrationThread = None
        self.systemStatus = False
        self.serverStatus = False
        #self.igtTimer = QtCore.QTimer()
        #self.igtTimer.timeout.connect(self.checkForIncomingMessage)
        #self.igtTimer.start(150)
        self.mode = MODE_IDLE
        self.systemMonitor = None
        self.subscriptions = []

    '''----------------------------------------------------------------------------'''
    '''--------------------------SYSTEM CALLS FUNCTIONS----------------------------'''
    '''----------------------------------------------------------------------------'''

    '''----------------------------------------------------------------------------'''
    '''                                TRACKING                                    '''
    '''----------------------------------------------------------------------------'''
    @pyqtSlot(list, list, int)
    def startTracking(self, sensorNames, ports, sliderPos):
        if self.mode == MODE_IDLE:
            selectedSensors = []
            selectedSensorNames = []
            selectedChannels = []
            selectedPorts = []
            config = guiutils.import_default_config_settings()

            for index, (sensorName, port) in enumerate(zip(sensorNames, ports)):
                if port is True:
                    portNo = index + 1
                    channel = config['system']['channels'][portNo-1]
                    sensor_settings = utils.import_sensor_settings(sensorName)
                    if sensor_settings is not None:
                        sensor = Sensor(sensor_settings)
                        sensor.channel = channel
                        selectedChannels.append(channel)
                        selectedSensors.append(sensor)
                        selectedSensorNames.append(sensorName)
                        selectedPorts.append(portNo)


            if len(selectedSensors) == 0:
                logging.info('No ports or sensors were selected')
            elif len(selectedSensorNames) != len(set(selectedSensorNames)):
                logging.info('Duplicate sensors selected')
            elif config is not None:
                config['system']['speed'] = sliderPos
                config['system']['channels'] = selectedChannels
                try:
                    self.anser = EMTracker(config)
                    self.anser.sensors = selectedSensors
                    self.anser.start_acquisition()
                    # system object so we can populate views
                    System_Template = namedtuple('System', ['freq', 'coils', 'sampling_freq', 'num_samples', 'ports', 'channels'])
                    system = System_Template(freq=[freq / 1000 for freq in self.anser.filter.transFreqs],
                                    coils=[True]*8,
                                    sampling_freq=self.anser.filter.sampleFreq,
                                    num_samples=self.anser.filter.numSamples,
                                    ports=selectedPorts,
                                    channels=self.anser.filter.channels)

                    qtScheduler = QtScheduler(QtCore)
                    newScheduler = NewThreadScheduler()
                    self.systemMonitor = Monitor(self.anser)
                    self.subscriptions.append(self.anser.positionNotifications.sample(15, scheduler=qtScheduler).subscribe(self.sendPositions))
                    self.subscriptions.append(self.anser.sampleNotifications.sample(30, scheduler=qtScheduler).subscribe(self.sendSamples))
                    self.subscriptions.append(self.anser.sampleNotifications.sample(1300, scheduler=newScheduler)\
                        .subscribe(on_next=self.systemMonitor.run_system_test))
                    self.subscriptions.append(self.systemMonitor.systemNotifications.subscribe_on(scheduler=qtScheduler)\
                        .subscribe(on_next=self.SYS_EVENT_SYSTEM_STATUS_NOTIFICATION.emit))
                    self.anser.start()
                    self.systemStatus = True
                    self.SYS_EVENT_SYSTEM_STATUS.emit(self.systemStatus)
                    self.SYS_EVENT_MODE_TRACKING.emit(system)
                    self.mode = MODE_TRACKING
                    self.SYS_EVENT_MODE_CHANGED.emit(self.mode)
                    logging.info('Started Tracking')
                except Exception as e:
                    logging.info('Device cannot be accessed. Possible causes: '
                                 '\n - Computer is not connected to DAQ port '
                                 '\n - After plugging device into the USB Port, '
                                 'wait a few moments  to let the driver install'
                                 '\n - Ensure device specified is correct. '
                                 '\n (Go to -> Developer Tab, in the configuration file under \'system\' change the \'device_name\' to your DevX indentifier) \n')
                    print(str(e))
            else:
                logging.info('No configuration file found. Go to -> Developer Tab and select configuration file. Click Make Default.')
        elif self.mode == MODE_TRACKING:
            self.stopTracking()
            logging.info('Stopped Tracking')
        else:
            logging.info('System is currently in use. Please stop calibration to continue')

    @pyqtSlot()
    def stopTracking(self):
        if self.anser is not None:
            self.anser.stop()
            list(map(lambda sub: sub.dispose(), self.subscriptions))
            self.systemMonitor = None
            self.stopServer()
            try:
                self.anser.stop_acquisition()
            except Exception as e:
                print(str(e))
            self.anser = None
            self.systemStatus = False
            self.SYS_EVENT_SYSTEM_STATUS.emit(self.systemStatus)
            self.mode = MODE_IDLE
            self.SYS_EVENT_MODE_CHANGED.emit(self.mode)
            self.SYS_EVENT_SYSTEM_STATUS_NOTIFICATION.emit(SystemStatusNotification(message='IDLE'))

    def sendPositions(self, positions):
        if self.anser is not None:
            xyz_positions = []
            for position in positions:
                xyz_position = [i * 1000 for i in position]
                #xyz_positions.append(xyz_position[:-2])
                xyz_positions.append(xyz_position)
            self.SYS_EVENT_POSITIONS_ACQUIRED.emit(xyz_positions)

    def sendSamples(self, samples):
        if self.anser is not None:
            self.SYS_EVENT_SAMPLES_ACQUIRED.emit(samples, self.anser.filter.sampleFreq)

    '''----------------------------------------------------------------------------'''
    '''                                CALIBRATION                                 '''
    '''----------------------------------------------------------------------------'''
    @pyqtSlot(str, int)
    def startCalibration(self, sensorName, port):
        if self.mode == MODE_IDLE:
            try:
                config = guiutils.import_default_config_settings()
                channel = config['system']['channels'][port-1]
                sensor_settings = utils.import_sensor_settings(sensorName)
                sensor = Sensor(sensor_settings)
                sensor.channel = channel
                calibration = EMCalibration(sensor, config)

                qtScheduler = QtScheduler(QtCore)
                newScheduler = NewThreadScheduler()
                self.systemMonitor = Monitor(calibration.anser)
                self.subscriptions.append(calibration.anser.sampleNotifications.sample(500, scheduler=newScheduler)\
                    .subscribe(self.systemMonitor.run_system_test))
                self.subscriptions.append(self.systemMonitor.systemNotifications.subscribe_on(scheduler=qtScheduler)\
                    .subscribe(self.SYS_EVENT_SYSTEM_STATUS_NOTIFICATION.emit))

                #remove this
                for i in range(3):
                    calibration.anser.sample_update()

                self.calibrationThread = CalibrationThread(calibration,
                                                           self.SYS_EVENT_POINT_CAPTURED,
                                                           self.SYS_EVENT_READY_TO_CALIBRATE,
                                                           self.SYS_EVENT_CALIBRATION_COMPLETED)
                self.calibrationThread.start()
                self.systemStatus = True
                self.SYS_EVENT_SYSTEM_STATUS.emit(self.systemStatus)
                self.SYS_EVENT_MODE_CALIBRATION.emit()
                self.SYS_EVENT_POINT_CAPTURED.emit(1)
                self.mode = MODE_CALIBRATING
                self.SYS_EVENT_MODE_CHANGED.emit(self.mode)

                logging.info('Started Calibration')
            except Exception as e:
                logging.info('Device cannot be accessed. Possible causes: '
                             '\n - Computer is not connected to DAQ port '
                             '\n - After plugging device into the USB Port, '
                             'wait a few moments  to let the driver install'
                             '\n - Ensure device specified is correct. '
                             '\n (Go to -> Developer Tab, in the configuration file under \'system\' change the \'device_name\' to your DevX indentifier) \n')
                print(str(e))
        elif self.mode == MODE_CALIBRATING:
            self.stopCalibration()
        else:
            logging.info('System is currently in use. Please stop tracking to continue')

    @pyqtSlot()
    def stopCalibration(self):
        self.SYS_EVENT_SENSORS_CHANGED.emit(self.getSensors())
        list(map(lambda sub: sub.dispose(), self.subscriptions))
        try:
            self.calibrationThread.emtrackerCalibration.reset()
            self.calibrationThread.terminate()
        except Exception as e:
            print(str(e))
        self.calibrationThread = None
        self.systemMonitor = None
        self.systemStatus = False
        self.mode = MODE_IDLE
        self.SYS_EVENT_SYSTEM_STATUS.emit(self.systemStatus)
        self.SYS_EVENT_MODE_CHANGED.emit(self.mode)
        self.SYS_EVENT_SYSTEM_STATUS_NOTIFICATION.emit(SystemStatusNotification(message='IDLE'))
        logging.info('Stopped Calibration')

    @pyqtSlot()
    def capturePoint(self):
        if self.calibrationThread is not None:
            self.calibrationThread.capture()

    @pyqtSlot()
    def calibrate(self):
        if self.calibrationThread is not None:
            self.calibrationThread.calibrate()

    '''----------------------------------------------------------------------------'''
    '''                                 NETWORKING                                 '''
    '''----------------------------------------------------------------------------'''

    @pyqtSlot(str, bool)
    def startServer(self, port, localhost):
        if self.mode == MODE_TRACKING and self.serverStatus is False:
            if self.anser is not None:
                if port.isdigit():
                    port = int(port)
                    try:
                        self.anser.create_igt_server(port, localhost)
                        self.serverStatus = True
                        self.SYS_EVENT_SERVER_STATUS.emit(True)
                        logging.info('Started Server')
                    except Exception as e:
                        logging.error('Error starting server')
        else:
            logging.info('Stopped Server')
            self.stopServer()

    def stopServer(self):
        if self.anser is not None:
            if self.anser.reset_server() is True:
                self.serverStatus = False
                self.SYS_EVENT_SERVER_STATUS.emit(False)

    #TODO: change this to use Rxpy rather than QTimer
    @pyqtSlot()
    def checkForIncomingMessage(self):
        if self.anser is not None:
            message = self.anser.get_network_message()
            if message is not None:
                self.SYS_EVENT_NETWORK_MSG_RECEIVED.emit(utils.convert_igt_message_to_text(message))

    '''----------------------------------------------------------------------------'''
    '''                                   SENSORS                                  '''
    '''----------------------------------------------------------------------------'''
    @pyqtSlot(str, str, str)
    def createNewSensor(self, name, description, dof):
        utils.add_sensor(name, description, dof)
        self.SYS_EVENT_SENSORS_CHANGED.emit(self.getSensors())

    @pyqtSlot(str)
    def removeSensor(self, name):
        utils.remove_sensor(name)
        self.SYS_EVENT_SENSORS_CHANGED.emit(self.getSensors())

    def getSensors(self):
        return utils.get_sensors()
