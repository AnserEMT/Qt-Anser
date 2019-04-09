""" The primary window and user interface for the application """
from PyQt5.QtWidgets import QMainWindow, QLabel, QDockWidget, QMenu, QAction
from PyQt5.QtCore import Qt, pyqtSlot
import qdarkstyle
from scipy import *
import logging
from app.gui.widgets.loggerwidget import LoggerWidget
from app.gui.widgets.tabwidget import TabWidget
import app.utilities.guiutils as guiutils


class MainWindow(QMainWindow):
    """ The primary window and user interface for the application.
    It contains:
        | four tabs - Visualisation, Tracking, Calibration, Settings
        | Status Bar - displays important system information
        | Logger - logs debug information for troubleshooting
        | Controller - to invoke EMT system functions
    """
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUI()
        defaultConfig = guiutils.get_settings_default_config()
        self.setStatusbarDefaultConfig(defaultConfig)

    def setupUI(self):
        """ Set ups the mainwindow by adding the status bar, logger widget and tabs."""
        # Setup the status bar. It contains the following parameters
        # Default Config, EMT System Mode (CAL, TRK, IDLE)
        # EMT System Status (OFF, ON, FAULT), Server Status (OFF, ON)
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
        self.setStatusbarSystemLED(False)
        self.statusBar().addPermanentWidget(self.statusBarSystemLED)
        self.statusBar().addPermanentWidget(QLabel('      '))
        self.statusBar().addPermanentWidget(QLabel('Server Status: '))
        self.statusBarServerLED = QLabel('')
        self.setStatusbarServerLED(False)
        self.statusBar().addPermanentWidget(self.statusBarServerLED)

        # Setup the Logger Widget
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

        # Add all tabs (visualisation, tracking, calibration, developer (ConfigEditor))
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

    @pyqtSlot()
    def changeTheme(self):
        """ Changes the colour of the mainwindow. Application must be restarted before the new theme can take effect. """
        dark_stylesheet = qdarkstyle.load_stylesheet_pyqt5()
        if self.styleSheet() != dark_stylesheet:
            self.setStyleSheet(dark_stylesheet)
        else:
            self.setStyleSheet('')

    @pyqtSlot()
    def changeFullScreen(self):
        """ Enables Fullscreen mode """
        self.showNormal() if self.isFullScreen() else self.showFullScreen()

    @pyqtSlot(object)
    def notificationHanlder(self, notification):
        """ Updates tracking side panel and status bar when a system notification is received

        :param notification: a notification which bundles EMT coil and system activity e.g system status code and message, coils status
        """
        self.setStatusbarSystemLEDByID(notification.status)
        self.setStatusbarMessage(notification.message)
        self.systemPanel.setCoilLEDsByID(notification.coils)
        # print('notification' + str(time.time()))

    @pyqtSlot(str)
    def changeDefaultConfig(self, file):
        """ Changes the default config file

        :param file: the name of the new default config file
        """
        if guiutils.set_settings_default_config(file):
            self.setStatusbarDefaultConfig(file)
            logging.info('Default configuration file has been changed: {}'.format(file))

    @pyqtSlot(str)
    def setStatusbarMessage(self, message):
        """ Updates the message (on the status bar)

        :param message: the given message to display
        """
        self.statusBar().clearMessage()
        message = 'STATUS: {}'.format(message)
        self.statusBar().showMessage(message)

    @pyqtSlot(bool)
    def setStatusbarSystemLED(self, status):
        """ Updates the system status LED (on the status bar)

        :param status: a boolean indicating the status of the system
        """
        self.statusBarSystemLED.setPixmap(guiutils.get_status_pixmap(status))

    @pyqtSlot(object)
    def setStatusbarSystemLEDByID(self, statusID):
        """ Updates the system status LED by ID (on the status bar)

        :param statusID: the given ID indicating the status of the LED
        """
        self.statusBarSystemLED.setPixmap(guiutils.get_status_pixmap_by_ID(statusID))

    @pyqtSlot(bool)
    def setStatusbarServerLED(self, status):
        """ Updates the OpenIGTLink server status LED (on the status bar)

        :param status: a boolean indicating the status of the OpenIGTLink server
        """
        self.statusBarServerLED.setPixmap(guiutils.get_status_pixmap(status))

    def setStatusbarDefaultConfig(self, file):
        """ Sets the name of the default config file (on the status bar)

        :param file: the name of the default config file
        """
        self.statusBarDefaultConfigLabel.setText(file)

    @pyqtSlot(str)
    def setStatusbarMode(self, mode):
        """ Sets the EMT mode (on the status bar)

        :param mode: the current EMT Mode (CAL,TRK,IDLE)
        """
        self.statusBarModeLabel.setText(mode)

    @pyqtSlot()
    def closeApplication(self):
        """ Closes the Anser application """
        sys.exit()


