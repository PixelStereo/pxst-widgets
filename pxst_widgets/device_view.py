#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
A DeviceView represents a bunch of parameters
It is designed to display instruments through remotes
"""

from pxst_widgets.panel import Panel
from pyossia import ossia
from PyQt5.Qt import QTimer, QThread, pyqtSignal



class DeviceUpdater(QThread):
    """
    Run a Device update queue
    """
    param_update = pyqtSignal(ossia.Parameter, object)
    def __init__(self, parent):
        super(DeviceUpdater, self).__init__()
        self.msgq = parent.msgq
        self.updater = None
        self.start()

    def __del__(self):
        self.wait()

    def run(self):
        while True:
            param_update = self.msgq.pop()
            if param_update != None:
                parameter, value = param_update
                self.param_update.emit(parameter, value)

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
        self.updater = DeviceUpdater(self)
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
            self.updater.param_update.connect(self.parameter_update)
            # REFLECT STATE
            remote.new_value(param.value)
            self.layout.addWidget(remote)

    def parameter_update(self, parameter, value):
        """
        This function is called by the Libossia messageQueue
        When a parameter which is registered to have a new value
        """
        # Check if the new value is different
        if self.view_db[parameter].getUI() != value:
            self.view_db[parameter].new_value(value)

    def resize(self, mode='auto'):
        """
        resize the DeviceView from its parameter size
        """
        if mode == 'auto':
            self.setFixedHeight(len(self.device.root_node.get_parameters()) * 69)
            self.setFixedWidth(305)
