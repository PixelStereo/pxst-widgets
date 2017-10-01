#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
This file is an example of a device
with I/O communication provided by libossia with pyqt5 GUI
"""

from pyossia import *
from pxst_widgets import *
from pxst_widgets.valueUI import *
from pxst_widgets.canvas import *

import sys

from PyQt5.QtCore import QFileInfo, Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QGroupBox, QHBoxLayout, QSlider, QLabel, QLineEdit, QCheckBox, QAbstractSlider, QMainWindow


# create the OSSIA Device with the name provided
# here for test purpose
my_device = ossia.LocalDevice('PyOssia Device')
my_device.expose(protocol='oscquery', udp_port=3456, ws_port=5678)
my_int = my_device.add_param('test/value/int', value_type='int', default=66)
my_float = my_device.add_param('test/value/float', value_type='float', default=0.123456789)
my_bool = my_device.add_param('test/value/bool', value_type='bool', default=True)
my_string = my_device.add_param('test/value/string', value_type='string', default='Hello world !')
my_vec3f = my_device.add_param('test/value/vec3f', value_type='vec3f', default=(0, 0.57, 0.81))
my_list = my_device.add_param('test/value/list', value_type='list', default=[44100, "my_track.wav", 0.6])

my_bool.value = ossia.Value(True)
my_float.value = ossia.Value(2.22)
my_int.value = ossia.Value(222)
my_string.value = ossia.Value('hello world!')
my_vec3f.value = ossia.Value([0, 0.57, 0.81])
my_list.value = ossia.Value([ossia.Value(44100), ossia.Value('my_track.wav'), ossia.Value(0.6)])

# create the UI now
# this could be another app that control the Pyossia Test Device

class MainWindow(QMainWindow):
    """
    Main Window Doc String
    """
    def __init__(self):
        super(MainWindow, self).__init__()
        # read a css for the whole MainWindow
        qss = open("style.qss", "r").read()
        self.setStyleSheet(qss)
        self.setAutoFillBackground(True)
        # Draw an UI for my_device
        self.canvas = Canvas(device=my_device, width='auto', height='auto')
        # assign this device to the mainwindow
        self.setCentralWidget(self.canvas)
        #self.setMinimumSize(self.canvas.width() + 10, self.canvas.height() + 10)
        self.move(0, 40)
        self.setFixedSize(self.centralWidget().width(), self.centralWidget().height())
        self.show()


if __name__ == "__main__":
    # this is for python2 only
    try:
        reload(sys)
        sys.setdefaultencoding('utf8')
    except NameError:
        pass
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    sys.exit(app.exec_())
