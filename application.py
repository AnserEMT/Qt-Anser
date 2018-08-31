'''Runs the application'''
import sys
try:
    sys.path.index('./python-anser/')
except ValueError:
    sys.path.append('./python-anser/')

from app.mainwindow import MainWindow
from app.qtanser import QtAnser
import app.utilities.guiutils as guiutils
import sys
from PyQt5.QtCore import QSettings
from PyQt5.QtWidgets import QApplication, QStyleFactory
from PyQt5.QtGui import QIcon
from PyQt5.Qt import QSize
from app.maincontroller import MainController
import os


class Application(QApplication):
    '''Responsible for instantiating application and main settings.'''
    def __init__(self, sys_argv):
        super(Application, self).__init__(sys_argv)
        self.setApplicationName("Anser")
        self.setOrganizationName("Anser")
        QSettings.setDefaultFormat(QSettings.IniFormat)
        #settings = QSettings()
        #print(str(QSettings.fileName(settings)))
        self.view = MainWindow()
        self.system = QtAnser()
        self.controller = MainController(self.view, self.system)
        self.view.show()



if __name__ == '__main__':
    app = Application(sys.argv)
    app_icon = QIcon()
    app_icon.addFile(guiutils.get_logo(), QSize(60, 60))
    app.setWindowIcon(app_icon)
    app.setStyle(QStyleFactory.create('Fusion'))
    sys.exit(app.exec_())