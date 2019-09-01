#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
This file is an example of a PyQt5 / OSCQuery Device
"""

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QHBoxLayout, QWidget
from pxst_widgets.device_view import DeviceView

# create the OSSIA Device and some parameters
from pyossia import *
# create the OSSIA Device with the name provided
my_device = ossia.LocalDevice('PyOssia Test Device')
my_device.expose(protocol='oscquery', listening_port=3456, sending_port=5678, logger=True)
#my_device.expose(protocol='osc', listening_port=11111, sending_port=22222, logger=False)
my_int = my_device.add_param('test/numeric/int', value_type='int', default_value=66, domain=[-100, 100], description='an integer')

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
        print(3)
        self.layout = QHBoxLayout()
        self.layout.addWidget(self.panel)
        main_box = QWidget()
        main_box.setLayout(self.layout)
        # assign this device to the mainwindow
        self.setCentralWidget(main_box)
        self.move(0, 40)
        #self.setMinimumSize(self.panel.width() + 10, self.panel.height() + 10)
        #self.setMinimumSize(self.centralWidget().width(), self.centralWidget().height())

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
