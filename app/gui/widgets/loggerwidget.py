from PyQt5.QtWidgets import QPlainTextEdit
import logging


class LoggerWidget(logging.Handler):
    '''
    Logs debug information which can be used for troubleshooting.
    '''
    def __init__(self, parent):
        super().__init__()
        self.widget = QPlainTextEdit(parent)
        self.widget.setReadOnly(True)
        self.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

    def emit(self, record):
        msg = self.format(record)
        self.widget.appendPlainText(msg)

    def write(self, m):
        pass
