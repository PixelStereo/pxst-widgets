#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
This file is an example of a device
with I/O communication provided by libossia with pyqt5 GUI
"""

import sys
import pxst_widgets
from pyossia import ossia
from zeroconf import ServiceBrowser, Zeroconf
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
from PyQt5.Qt import pyqtSignal, QObject, QThread
from pxst_widgets.device_view import DeviceView


class ZeroConfListener(QThread):
    add_device = pyqtSignal(str, str, int)
    remove_device = pyqtSignal(str)
    def __init__(self, *args, **kwargs):
        super(ZeroConfListener, self).__init__()
        self.__devices__ = {}
        zeroconf = Zeroconf()
        browser = ServiceBrowser(zeroconf, "_oscjson._tcp.local.", self)

    def remove_service(self, zeroconf, type, name):
        name = name.split('.' + type)[0]
        self.__devices__.pop(name)
        self.remove_device.emit(name)

    def add_service(self, zeroconf, type, name):
        info = zeroconf.get_service_info(type, name)
        name = name.split('.' + type)[0]
        port = info.port
        server = info.server
        self.__devices__.setdefault(name, {'server': server, 'port':port})
        self.add_device.emit(name, server, port)


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
        #self.move(0, 40)
        # start the callback, it will create items
        listener = ZeroConfListener()
        listener.add_device.connect(self.add_device)
        listener.remove_device.connect(self.remove_device)

    def add_device(self, name, server, port):
        print('yeah')
        try:
            target = 'ws://' + server + ':' + str(port)
            mirror_device = ossia.OSCQueryDevice("Explorer for " + name, target, 5678)
            print('OK, device ready')
        except RuntimeError:
            print('Exception raised. Is it the best way?')
            target = 'http://' + server + ':' + str(port)
            mirror_device = ossia.OSCQueryDevice("Explorer for " + name, target, 5678)
                # Grab the namespace with an update
        print('update it now')
        mirror_device.update()
        description = name + ' on ' + server + ':' + str(port)
        print('ADDED ' + str(name))
        # Draw an UI for local_device
        self.panel = DeviceView(device=mirror_device, width='auto', height='auto')
        # assign this device to the mainwindow
        self.setCentralWidget(self.panel)
        self.setFixedSize(self.centralWidget().width(), self.centralWidget().height())

    def remove_device(self, name):
        print('BYE BYE ' + name)


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
