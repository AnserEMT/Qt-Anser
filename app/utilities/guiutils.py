from PyQt5.QtCore import Qt, QSettings
from PyQt5.QtGui import QPixmap
## Anser Import
import utils.utils as utils
OFF = 0
FAULT = 1
ON = 2


def get_status_pixmap(status):
    if status is True:
        return QPixmap(utils.resource_path('./app/resources/icons/button-green.png')).scaled(16, 16, Qt.KeepAspectRatio)
    else:
        return QPixmap(utils.resource_path('./app/resources/icons/button-grey.png')).scaled(16, 16, Qt.KeepAspectRatio)

def get_status_pixmap_by_ID(statusID):
    if statusID == OFF:
        return QPixmap(utils.resource_path('./app/resources/icons/button-grey.png')).scaled(16, 16, Qt.KeepAspectRatio)
    elif statusID == FAULT:
        return QPixmap(utils.resource_path('./app/resources/icons/button-orange.png')).scaled(16, 16, Qt.KeepAspectRatio)
    elif statusID == ON:
        return QPixmap(utils.resource_path('./app/resources/icons/button-green.png')).scaled(16, 16, Qt.KeepAspectRatio)



def get_logo():
    return utils.resource_path('./app/resources/icons/anser_logo.png')


def get_settings_default_config():
    settings = QSettings()
    defaultConfig = settings.value('default_config', type=str)
    if defaultConfig == '':
        return 'None'
    return defaultConfig


def set_settings_default_config(filename):
    try:
        settings = QSettings()
        settings.setValue("default_config", filename)
    except Exception as e:
        print(str(e))
        return False
    return True


def import_default_config_settings():
    settings = QSettings()
    defaultConfigName = settings.value('default_config', type=str)
    return utils.import_config_settings(defaultConfigName)

def get_board_dimensions():
    #TODO: fix this
    settings = QSettings()
    defaultConfigName = settings.value('default_config', type=str)
    config = utils.import_config_settings(defaultConfigName)
    if config is not None:
        boardType = config['system']['device_cal']
        return (9, 9) if boardType == '9x9' else (7, 7)
    else:
        return (7, 7)
