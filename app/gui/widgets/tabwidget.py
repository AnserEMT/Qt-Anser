'''The container of all tabs'''
from PyQt5.QtWidgets import QTabWidget
from app.gui.tabs.systemtab import SystemTab
from app.gui.tabs.igttab import IGTTab
from app.gui.tabs.calibrationtab import CalibrationTab
from app.gui.tabs.configeditortab import ConfigEditorTab

IGT_TAB = 0
SYSTEM_TAB = 1
CALIBRATION_TAB = 2
DEVELOPER_TAB = 3


class TabWidget(QTabWidget):
    '''
    Container for the visualisation, tracking, calibration and settings tabs.
    Most tabs house a specialised widget such as a graph (left) and a side panel (right).
    '''
    def __init__(self):
        super(TabWidget, self).__init__()
        self.igttab = IGTTab()
        self.systemtab = SystemTab()
        self.calibrationtab = CalibrationTab()
        self.developertab = ConfigEditorTab()
        self.addTab(self.igttab, "Server")
        self.addTab(self.systemtab, "Tracking")
        self.addTab(self.calibrationtab, 'Calibration')
        self.addTab(self.developertab, "Developer")

