#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
A DeviceView represents a bunch of parameters
It is designed to display instruments through remotes
"""

from pxst_widgets.panel import Panel
from pyossia import ossia
from PyQt5.QtCore import Qt
from PyQt5.Qt import QTimer, QThread, pyqtSignal, QPalette
from PyQt5.QtWidgets import QGroupBox, QGridLayout
from pxst_widgets.inspector import ParameterView


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
        self.selected = None
        self.view_db = {}
        self.updater = None
        self.inspector = ParameterView(None)
        self.layout.addWidget(self.inspector, 0, 0)
        self.parameters = QGroupBox('parameters available')
        self.parameters_layout = QGridLayout()
        self.parameters.setLayout(self.parameters_layout)
        self.layout.addWidget(self.parameters, 1, 0)
        self.setup(kwargs)

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
        for param in self.device.root_node.get_parameters():
            # create the UI for this parameter
            remote = self.add_remote(param)
            remote.selection_update.connect(self.selection_changed)
            remote.setStyleSheet("""
               QGroupBox 
               { 
                   border:1px solid rgb(216, 216, 216); 
               }
               """
            )
            # register this view in the view list
            self.view_db.setdefault(param, remote)
            # request for signal updates
            self.msgq.register(param)
            # connect the updater thread to this remote
            self.updater.param_update.connect(self.parameter_update)
            # update current state
            remote.new_value(param.value)
            # add the remote to the layout
            self.parameters_layout.addWidget(remote)

    def selection_changed(self, parameter):
        """
        a parameter has been selected by clicking inside its groupbox
        """
        # Release last selection
        if self.selected:
            ui = self.view_db[self.selected]
            ui.setStyleSheet("""
                QGroupBox 
                { 
                    border:1px solid rgb(216, 216, 216); 
                }
                """
            )
        self.inspector.inspect(parameter)
        ui = self.view_db[parameter]
        self.selected = parameter
        ui = self.view_db[parameter]
        ui.setStyleSheet("""
           QGroupBox 
           { 
               border:1px solid rgb(0, 146, 207); 
           }
           """
        )


    def parameter_update(self, parameter, value):
        """
        This function is called by the Libossia messageQueue
        When a parameter which is registered to have a new value
        """
        # Check if the new value is different
        if self.view_db[parameter].getUI() != value:
            self.view_db[parameter].new_value(value)
