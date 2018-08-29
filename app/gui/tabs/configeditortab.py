from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QStandardItemModel, QStandardItem
import ruamel.yaml as ruamel_yaml
# Anser imports
import utils.utils as utils


class ConfigEditorTab(QWidget):
    '''
    Allows the user to change EMT system settings by editing configuration files.
    '''
    UI_REQUEST_CHANGE_DEFAULT_CONFIG = pyqtSignal(str)

    def __init__(self):

        super(ConfigEditorTab, self).__init__()

        self.data = None
        applyButton = QPushButton("Apply Changes")
        self.combobox = QComboBox()

        self.defaultButton = QPushButton('Make Default')


        buttonLayout = QHBoxLayout()
        buttonLayout.addWidget(self.combobox,  0, Qt.AlignLeft)
        buttonLayout.addWidget(self.defaultButton, 0, Qt.AlignLeft)
        buttonLayout.addStretch(1)
        buttonLayout.addWidget(applyButton, 0, Qt.AlignRight )

        self.tree = QTreeView()

        mainLayout = QVBoxLayout()
        mainLayout.addLayout(buttonLayout)
        mainLayout.addWidget(self.tree)
        self.setLayout(mainLayout)
        self.setGeometry(300, 300, 600, 400)

        applyButton.clicked.connect(self.saveChanges)
        self.combobox.currentIndexChanged.connect(self.refresh)
        self.defaultButton.clicked.connect(lambda: self.UI_REQUEST_CHANGE_DEFAULT_CONFIG.emit(self.combobox.currentText()))

        self.populateCombos()
        self.data = utils.import_config_settings(self.combobox.currentText())

        # Tree view
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
        self.tree.setModel(None)
        self.tree.setModel(QStandardItemModel())
        self.tree.setAlternatingRowColors(True)
        # self.tree.setSortingEnabled(True)
        self.tree.setHeaderHidden(False)
        self.tree.setSelectionBehavior(QAbstractItemView.SelectItems)
        self.tree.model().setHorizontalHeaderLabels(['Parameter', 'Value'])
        self.tree.setColumnWidth(0, 200)
        self.data = utils.import_config_settings(self.combobox.itemText(i))
        self.tree.model().itemChanged.connect(self.handleItemChanged)
        self.loadData()
        self.tree.expandAll()

    def printData(self):
        print(str(self.data))

    def loadData(self):
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
        for file in utils.get_all_config_files():
            self.combobox.addItem(file.title(), file)

    def saveChanges(self):
        filename = self.combobox.currentText()
        filepath = utils.get_config_filepath(filename)
        utils.export_settings(self.data, filepath)

    def handleItemChanged(self, item):
        parent = self.data[item.parent().text()]
        key = item.parent().child(item.row(), 0).text()
        try:
            parent[key] = ruamel_yaml.load(item.text(),  Loader=ruamel_yaml.Loader)
        except Exception as e:
            print("error error", e)
            self.refresh(self.combobox.currentIndex())
