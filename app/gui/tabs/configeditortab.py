""" Edit EMT system settings """
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QStandardItemModel, QStandardItem
import ruamel.yaml as ruamel_yaml
# Anser imports
import utils.utils as utils


class ConfigEditorTab(QWidget):
    """
    Allows the user to change EMT system settings by editing configuration files *(config.yaml)*.
    The user can use the combobox to select and view different config files.
    """

    #: **(QtSignal) UI request:** to change the default config file
    UI_REQUEST_CHANGE_DEFAULT_CONFIG = pyqtSignal(str)
    def __init__(self):
        super(ConfigEditorTab, self).__init__()
        # stores all the data for the current config file
        self.data = None
        # applyButton - saves any changes made to the config file
        applyButton = QPushButton("Apply Changes")
        applyButton.clicked.connect(self.saveChanges)

        # defaultButton - makes the current config file the default config file.
        self.defaultButton = QPushButton('Make Default')
        self.defaultButton.clicked.connect(lambda: self.UI_REQUEST_CHANGE_DEFAULT_CONFIG.emit(self.fileCombobox.currentText()))

        # fileCombobox -  allows the user to select and view different config files
        self.fileCombobox = QComboBox()
        self.fileCombobox.currentIndexChanged.connect(self.refresh)

        buttonLayout = QHBoxLayout()
        buttonLayout.addWidget(self.fileCombobox, 0, Qt.AlignLeft)
        buttonLayout.addWidget(self.defaultButton, 0, Qt.AlignLeft)
        buttonLayout.addStretch(1)
        buttonLayout.addWidget(applyButton, 0, Qt.AlignRight )

        # The TreeView Widget provides textfields allowing the user to edit the config file
        self.tree = QTreeView()

        mainLayout = QVBoxLayout()
        mainLayout.addLayout(buttonLayout)
        mainLayout.addWidget(self.tree)
        self.setLayout(mainLayout)
        self.setGeometry(300, 300, 600, 400)

        self.populateCombos()

        # stores all the data for the current config file
        self.data = utils.import_config_settings(self.fileCombobox.currentText())

        self.tree.setModel(QStandardItemModel())
        self.tree.setAlternatingRowColors(True)
        #self.tree.setSortingEnabled(False)
        self.tree.setHeaderHidden(False)
        self.tree.setSelectionBehavior(QAbstractItemView.SelectItems)
        self.tree.model().setHorizontalHeaderLabels(['Parameter', 'Value'])
        self.tree.setColumnWidth(0, 200)
        self.tree.model().itemChanged.connect(self.handleItemChanged)
        self.loadData()
        self.tree.expandAll()

    def refresh(self, i):
        """ refreshes the TreeView Widget.
        Called when the user selects a different config file from the fileCombobox.

        :param i: current index of fileCombobox
        """
        self.tree.setModel(None)
        self.tree.setModel(QStandardItemModel())
        self.tree.setAlternatingRowColors(True)
        # self.tree.setSortingEnabled(True)
        self.tree.setHeaderHidden(False)
        self.tree.setSelectionBehavior(QAbstractItemView.SelectItems)
        self.tree.model().setHorizontalHeaderLabels(['Parameter', 'Value'])
        self.tree.setColumnWidth(0, 200)
        self.data = utils.import_config_settings(self.fileCombobox.itemText(i))
        self.tree.model().itemChanged.connect(self.handleItemChanged)
        self.loadData()
        self.tree.expandAll()

    def printData(self):
        """ prints the data of the current config file to console. """
        print(str(self.data))

    def loadData(self):
        """ loads the TreeView Widget with the data from the current config file. """
        try:
            for x in self.data:
                if not self.data[x]:
                    continue
                parent = QStandardItem(x)
                parent.setFlags(Qt.NoItemFlags)
                for y in self.data[x]:
                    value = self.data[x][y]
                    child0 = QStandardItem(y)
                    child0.setFlags(Qt.NoItemFlags | Qt.ItemIsEnabled)
                    child1 = QStandardItem(str(value))
                    child1.setFlags(Qt.ItemIsEnabled |Qt.ItemIsEditable | Qt.ItemIsSelectable)
                    parent.appendRow([child0, child1])
                self.tree.model().appendRow(parent)
        except Exception as e:
            print(str(e))

    def populateCombos(self):
        """ Populates the fileCombobox with all available config files. """
        for file in utils.find_all_configs():
            self.fileCombobox.addItem(file.title(), file)

    def saveChanges(self):
        """ Saves any changes made to the current config file. """
        filename = self.fileCombobox.currentText()
        filepath = utils.find_config(filename)
        utils.export_settings(self.data, filepath)

    def handleItemChanged(self, item):
        """ Called when a user modifies a textfield

        :param item: the given textfield """
        # Update data with text from textfield
        parent = self.data[item.parent().text()]
        key = item.parent().child(item.row(), 0).text()
        try:
            parent[key] = ruamel_yaml.load(item.text(),  Loader=ruamel_yaml.Loader)
        except Exception as e:
            print("error error", e)
            self.refresh(self.fileCombobox.currentIndex())
