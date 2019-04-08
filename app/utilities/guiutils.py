from PyQt5.QtCore import Qt, QSettings
from PyQt5.QtGui import QPixmap
## Anser Import
import utils.utils as utils
OFF = 0
FAULT = 1
ON = 2


def get_status_pixmap(status):
    """Get the coloured LED Pixmap for the given status (where OFF=Grey, ON=Green)

    :param status: a boolean indicating the status of the LED
    :return: a coloured pixmap
    """
    if status is True:
        return QPixmap(utils.resource_path('./app/resources/icons/button-green.png')).scaled(16, 16, Qt.KeepAspectRatio)
    else:
        return QPixmap(utils.resource_path('./app/resources/icons/button-grey.png')).scaled(16, 16, Qt.KeepAspectRatio)


def get_status_pixmap_by_ID(statusID):
    """ Get the coloured LED Pixmap for the given ID (where OFF=Grey(0), FAULT=ORANGE(1), ON=Green(2))
    :param statusID: the given ID indicating the status of the LED
    :return: QPixmap : a coloured pixmap
    """
    if statusID == OFF:
        return QPixmap(utils.resource_path('./app/resources/icons/button-grey.png')).scaled(16, 16, Qt.KeepAspectRatio)
    elif statusID == FAULT:
        return QPixmap(utils.resource_path('./app/resources/icons/button-orange.png')).scaled(16, 16, Qt.KeepAspectRatio)
    elif statusID == ON:
        return QPixmap(utils.resource_path('./app/resources/icons/button-green.png')).scaled(16, 16, Qt.KeepAspectRatio)


def get_logo():
    """ Get the path of the Anser Logo
    :return: the path of the Anser Logo
    """
    return utils.resource_path('./app/resources/icons/anser_logo.png')


def get_settings_default_config():
    """ Get the name of the default config file

    :return: the name of the default config file
    """
    settings = QSettings()
    defaultConfig = settings.value('default_config', type=str)
    if defaultConfig == '':
        return 'None'
    return defaultConfig


def set_settings_default_config(filename):
    """ Sets the name of the default config file in QSettings

    :param filename: the given filename
    :return: boolean indicating whether the name of the default config file has been saved
    """
    try:
        settings = QSettings()
        settings.setValue("default_config", filename)
    except Exception as e:
        print(str(e))
        return False
    return True


def import_default_config_settings():
    """ Returns all the settings for the default config file

    :return: the settings for the default config file
    """
    settings = QSettings()
    defaultConfigName = settings.value('default_config', type=str)
    return utils.import_config_settings(defaultConfigName)


def get_board_dimensions():
    """ Gets the current dimensions for the transmitter board (7x7, 9x9 .etc)

    :return: a list indicating the current dimensions for the transmitter board
    """
    #TODO: fix this
    settings = QSettings()
    defaultConfigName = settings.value('default_config', type=str)
    config = utils.import_config_settings(defaultConfigName)
    if config is not None:
        boardType = config['system']['device_cal']
        return (9, 9) if boardType == '9x9' else (7, 7)
    else:
        return (7, 7)
