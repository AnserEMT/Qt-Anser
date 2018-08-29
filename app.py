# include submodule python-anser in pythonpath
# Eventually, you will be able to import this as a python package
import sys
try:
    sys.path.index('./python-anser/')
except ValueError:
    sys.path.append('./python-anser/')

from app.mainwindow import MainWindow
from app.qtemt import QtEmt
import app.utilities.guiutils as guiutils
import sys
from PyQt5.QtCore import QSettings
from PyQt5.QtWidgets import QApplication, QStyleFactory
from PyQt5.QtGui import QIcon
from PyQt5.Qt import QSize
from app.maincontroller import MainController
import os


class App(QApplication):
    '''Responsible for instantiating application.'''
    def __init__(self, sys_argv):
        super(App, self).__init__(sys_argv)
        self.setApplicationName("Anser")
        self.setOrganizationName("Anser")
        QSettings.setDefaultFormat(QSettings.IniFormat)
        #settings = QSettings()
        #print(str(QSettings.fileName(settings)))
        self.view = MainWindow()
        self.system = QtEmt()
        self.controller = MainController(self.view, self.system)
        self.view.show()



if __name__ == '__main__':
    app = App(sys.argv)
    app_icon = QIcon()
    app_icon.addFile(guiutils.get_logo(), QSize(60, 60))
    app.setWindowIcon(app_icon)
    app.setStyle(QStyleFactory.create('Fusion'))
    sys.exit(app.exec_())