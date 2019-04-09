""" Qt interface for performing a calibration """
from PyQt5.QtCore import QThread
import threading


class CalibrationThread(QThread):
    """ A wrapper for the `emcalibration` class """
    def __init__(self, emCalibration, pointCapturedEvent, readyToCalibrateEvent, calibrationCompleteEvent):
        """
        :param emCalibration: `emCalibration` instance
        :param pointCapturedEvent: the pyqtSignal() signalling a point has been captured
        :param readyToCalibrateEvent: the pyqtSignal() signalling all points have been captured
        :param calibrationCompleteEvent: the pyqtSignal() signalling calibration has completed
        """
        super(CalibrationThread, self).__init__()
        self.emtrackerCalibration = emCalibration
        self.finalCapture = emCalibration.point_count
        self.captureEvent = threading.Event()
        self.calibrateEvent = threading.Event()
        self.nextCapturePointSignal = pointCapturedEvent
        self.readyToCalibrateSignal = readyToCalibrateEvent
        self.finishedCalibrationSignal = calibrationCompleteEvent

    def capture(self):
        if not self.captureEvent.is_set():
            self.captureEvent.set()

    def calibrate(self):
        if not self.calibrateEvent.is_set():
            self.calibrateEvent.set()

    def run(self):
        while True:
            self.captureEvent.clear()
            self.captureEvent.wait()
            nextCapture = self.emtrackerCalibration.next()
            self.nextCapturePointSignal.emit(nextCapture)
            if nextCapture > self.finalCapture:
                self.readyToCalibrateSignal.emit()
                self.calibrateEvent.clear()
                self.calibrateEvent.wait()
                self.emtrackerCalibration.calibrate()
                self.emtrackerCalibration.reset()
                self.finishedCalibrationSignal.emit()



