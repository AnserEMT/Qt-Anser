from PyQt5.QtWidgets import QMainWindow, QLabel, QDockWidget, QMenu, QAction
from PyQt5.QtCore import Qt, pyqtSlot
import qdarkstyle
from scipy import *
import logging
from app.gui.widgets.loggerwidget import LoggerWidget
from app.gui.widgets.tabWidget import TabWidget
import app.utilities.guiutils as guiutils


class MainWindow(QMainWindow):
    '''
    The primary window and user interface for the application.
    It contains:
        four tabs - Visualisation, Tracking, Calibration, Settings
        Status Bar - displays important system information
        Logger - logs debug information for troubleshooting
        Controller - to invoke EMT system functions

    '''
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUI()
        defaultConfig = guiutils.get_settings_default_config()
        self.setStatusBarDefaultConfig(defaultConfig)

    def setupUI(self):
        self.statusBar().addPermanentWidget(QLabel('Default Config: '))
        self.statusBarDefaultConfigLabel = QLabel('')
        self.statusBar().addPermanentWidget(self.statusBarDefaultConfigLabel)
        self.statusBar().addPermanentWidget(QLabel('      '))
        self.statusBar().addPermanentWidget(QLabel('Mode: '))
        self.statusBarModeLabel = QLabel('IDLE')
        self.statusBar().addPermanentWidget(self.statusBarModeLabel)
        self.statusBar().addPermanentWidget(QLabel('      '))

        self.statusBar().addPermanentWidget(QLabel('System Status: '))
        self.statusBarSystemLED = QLabel('')
        self.setStatusBarSystemLED(False)
        self.statusBar().addPermanentWidget(self.statusBarSystemLED)
        self.statusBar().addPermanentWidget(QLabel('      '))
        self.statusBar().addPermanentWidget(QLabel('Server Status: '))
        self.statusBarServerLED = QLabel('')
        self.setStatusBarLED(False)
        self.statusBar().addPermanentWidget(self.statusBarServerLED)

        self.dockableWidget = QDockWidget("Logger", self)
        self.addDockWidget(Qt.BottomDockWidgetArea, self.dockableWidget)
        self.loggerWidget = LoggerWidget(self)
        logging.getLogger().addHandler(self.loggerWidget)
        logging.getLogger().setLevel(logging.INFO)
        self.dockableWidget.setWidget(self.loggerWidget.widget)

        # Create menu options
        menubar = self.menuBar()
        menubar.setNativeMenuBar(False)
        fileMenu = QMenu('File', self)
        showConsoleAction = QAction('Show Console', self)
        showConsoleAction.triggered.connect(self.dockableWidget.show)
        changeThemeAction = QAction('Change Theme', self)
        changeThemeAction.triggered.connect(self.changeTheme)
        exitAction = QAction("Exit", self)
        exitAction.setShortcut("Ctrl+Q")
        exitAction.setStatusTip('Leave The App')
        exitAction.triggered.connect(self.closeApplication)
        fileMenu.addAction(showConsoleAction)
        fileMenu.addAction(changeThemeAction)
        fileMenu.addAction(exitAction)
        viewMenu = QMenu('View', self)
        fullscreenAction = QAction('Enter Full Screen', self)
        fullscreenAction.triggered.connect(self.changeFullScreen)
        viewMenu.addAction(fullscreenAction)
        menubar.addMenu(fileMenu)
        menubar.addMenu(viewMenu)

        self.tb = TabWidget()
        self.systemPanel = self.tb.systemtab.systemPanel
        self.fftGraph = self.tb.systemtab.fftGraph
        self.positionGraph = self.tb.igttab.positionGraph
        self.igtPanel = self.tb.igttab.igtPanel
        self.calibrationPanel = self.tb.calibrationtab.calibrationPanel
        self.gridGraph = self.tb.calibrationtab.gridwidget.graph
        self.configEditor = self.tb.developertab
        self.setCentralWidget(self.tb)
        self.setGeometry(50, 50, 1000, 1000)
        self.setWindowTitle("Anser")


    '''----------------------------------------------------------------------------'''
    '''------------------------------UI FUNCTIONS-----------------------------------'''
    '''----------------------------------------------------------------------------'''
    @pyqtSlot()
    def changeTheme(self):
        dark_stylesheet = qdarkstyle.load_stylesheet_pyqt5()
        if self.styleSheet() != dark_stylesheet:
            self.setStyleSheet(dark_stylesheet)
        else:
            self.setStyleSheet('')

    @pyqtSlot()
    def changeFullScreen(self):
        self.showNormal() if self.isFullScreen() else self.showFullScreen()

    @pyqtSlot(str)
    def setStatusBarMessage(self, message):
        self.statusBar().clearMessage()
        message = 'STATUS: {}'.format(message)
        self.statusBar().showMessage(message)

    @pyqtSlot(bool)
    def setStatusBarSystemLED(self, status):
        self.statusBarSystemLED.setPixmap(guiutils.get_status_pixmap(status))

    @pyqtSlot(object)
    def setStatusBarSystemLEDByID(self, statusID):
        self.statusBarSystemLED.setPixmap(guiutils.get_status_pixmap_by_ID(statusID))

    @pyqtSlot(bool)
    def setStatusBarLED(self, status):
        self.statusBarServerLED.setPixmap(guiutils.get_status_pixmap(status))

    def setStatusBarDefaultConfig(self, file):
        self.statusBarDefaultConfigLabel.setText(file)

    @pyqtSlot(str)
    def setStatusBarMode(self, mode):
        self.statusBarModeLabel.setText(mode)

    @pyqtSlot(object)
    def notificationHanlder(self, notification):
        self.setStatusBarSystemLEDByID(notification.status)
        self.setStatusBarMessage(notification.message)
        self.systemPanel.setCoilLEDsByID(notification.coils)
        #print('notification' + str(time.time()))

    @pyqtSlot()
    def closeApplication(self):
        sys.exit()

    @pyqtSlot(str)
    def changeDefaultConfig(self, file):
        if guiutils.set_settings_default_config(file):
            self.setStatusBarDefaultConfig(file)
            logging.info('Default configuration file has been changed: {}'.format(file))
