#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
A DeviceView represents a bunch of parameters
It is designed to display instruments through remotes
"""

from pxst_widgets.panel import Panel
from pyossia import ossia
from PyQt5.Qt import QTimer, QThread


class DeviceUpdater(QThread):
    """docstring for DeviceUpdater"""
    def __init__(self, parent):
        super(DeviceUpdater, self).__init__()
        self.msgq = parent.msgq
        self.view_db = parent.view_db
        self.start()

    def run(self):
        from time import sleep
        while True:
            param_update = self.msgq.pop()
            if param_update != None:
                print('-- something new --', param_update)
                parameter, value = param_update
                self.view_db[parameter].setValue(value)
            sleep(0.01)

    def __del__(self):
        self.wait()


class DeviceView(Panel):
    """
    PyQt DeviceView that display all params of a device
    float / int : QSlider + QSpiVBox
    string : QLineEdit
    bool : QCheckBox
    todo : tuples : depend of the unit (color, spatial, etc…)
    """
    def __init__(self, device, **kwargs):
        super(DeviceView, self).__init__()
        # create a layout for this groupbox (to attach widgets on)
        self.device = device
        self.view_db = {}
        self.updater = None
        self.setup(kwargs)
        self.resize()

    def setup(self, kwargs):
        """
        create a Remote for each parameter
        """
        self.msgq = ossia.MessageQueue(self.device)
        # set title for the DeviceView
        try:
            self.setTitle(self.device.name)
        except:
            self.setTitle(str(self.device))
        #self.setTitle(str(self.device.get_nodes()[0]))
        for param in self.device.root_node.get_parameters():
            remote = self.add_remote(param)
            self.view_db.setdefault(param, remote)
            self.msgq.register(param)
            # REFLECT STATE
            #remote.setValue(param.value)
            self.layout.addWidget(remote)
        self.updater = DeviceUpdater(self)

    def resize(self, mode='auto'):
        """
        resize the DeviceView from its parameter size
        """
        if mode == 'auto':
            self.setFixedHeight(len(self.device.root_node.get_parameters()) * 69)
            self.setFixedWidth(305)
