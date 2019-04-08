""" The container of all tabs """
from PyQt5.QtWidgets import QTabWidget
from app.gui.tabs.systemtab import SystemTab
from app.gui.tabs.visualisationtab import VisualisationTab
from app.gui.tabs.calibrationtab import CalibrationTab
from app.gui.tabs.configeditortab import ConfigEditorTab

IGT_TAB = 0
SYSTEM_TAB = 1
CALIBRATION_TAB = 2
DEVELOPER_TAB = 3


class TabWidget(QTabWidget):
    """
    Container for the visualisation, tracking, calibration and settings/developer tabs.
    Most tabs house a specialised widget such as a graph (left) and a side panel (right).
        | :mod:`~app.gui.tabs.visualisationtab` :mod:`~app.gui.tabs.calibrationtab` :mod:`~app.gui.tabs.configeditortab` :mod:`~app.gui.tabs.systemtab`
    """
    def __init__(self):
        super(TabWidget, self).__init__()
        # Tab 1: IGT
        self.igttab = VisualisationTab()
        # Tab 2: Tracking
        self.systemtab = SystemTab()
        # Tab 3: Calibration
        self.calibrationtab = CalibrationTab()
        # Tab 4: Developer / EMT System Settings
        self.developertab = ConfigEditorTab()
        self.addTab(self.igttab, "Visualisation")
        self.addTab(self.systemtab, "Tracking")
        self.addTab(self.calibrationtab, 'Calibration')
        self.addTab(self.developertab, "Developer")

