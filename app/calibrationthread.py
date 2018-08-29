from PyQt5.QtCore import QThread
import threading


class CalibrationThread(QThread):
    def __init__(self, emtrackerCalibration, pointCapturedEvent, readyToCalibrateEvent, calibrationCompleteEvent):
        super(CalibrationThread, self).__init__()
        self.emtrackerCalibration = emtrackerCalibration
        self.finalCapture = emtrackerCalibration.point_count
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



