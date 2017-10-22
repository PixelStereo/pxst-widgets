#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
This file is an example of a PyQt5 / OSCQuery Device
"""

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow

from pxst_widgets.device_view import DeviceView

# create the OSSIA Device and some parameters
from pyossia import *
# create the OSSIA Device with the name provided
my_device = ossia.LocalDevice('PyOssia Test Device')
my_device.expose(protocol='oscquery', listening_port=3456, sending_port=5678, logger=True)
#my_device.expose(protocol='osc', listening_port=11111, sending_port=22222, logger=False)
my_int = my_device.add_param('test/numeric/int', value_type='int', default_value=66, domain=[-100, 100])
my_float = my_device.add_param('test/numeric/float', value_type='float', default_value=0.123456789, domain=[-2, 2.2])
my_bool = my_device.add_param('test/special/bool', value_type='bool', default_value=True, repetitions_filter=True)
my_string = my_device.add_param('test/string', value_type='string', default_value='Hello world !', domain=['once', 'loop'])
my_list = my_device.add_param('test/list', value_type='list', default_value=[44100, "my_track.wav", 0.6])
my_char = my_device.add_param('test/special/char', value_type='char', default_value=chr(97))
my_vec2f = my_device.add_param('test/list/vec2f', value_type='vec2f', default_value=[0.5, 0.5])
my_vec3f = my_device.add_param('test/list/vec3f', value_type='vec3f', default_value=[-960, -270, 180],  domain=[0, 360])
my_vec4f = my_device.add_param('test/list/vec4f', value_type='vec4f', default_value=[0, 0.57, 0.81, 0.7],  domain=[0, 1])

my_device.root_node.init()

class MainWindow(QMainWindow):
    """
    Main Window Doc String
    """
    def __init__(self):
        super(MainWindow, self).__init__()
        # read a css for the whole MainWindow
        qss = open("style-.qss", "r").read()
        self.setStyleSheet(qss)
        self.setAutoFillBackground(True)
        # Draw an UI for my_device
        self.panel = DeviceView(my_device, width='auto', height='auto')
        # assign this device to the mainwindow
        self.setCentralWidget(self.panel)
        self.move(0, 40)
        #self.setMinimumSize(self.panel.width() + 10, self.panel.height() + 10)
        self.setFixedSize(self.centralWidget().width(), self.centralWidget().height())

if __name__ == "__main__":
    # this is for python2 only
    try:
        reload(sys)
        sys.setdefaultencoding('utf8')
    except NameError:
        pass
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())
