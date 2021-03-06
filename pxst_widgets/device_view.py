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
from pxst_widgets.inspector import ParameterView, DeviceInspector


class DeviceView(Panel):
    """
    PyQt DeviceView that display all params of a device
    float / int : QSlider + QSpiVBox
    string : QLineEdit
    bool : QCheckBox
    todo : tuples : depend of the unit (color, spatial, etc…)
    """
    def __init__(self, device, **kwargs):
        super(DeviceView, self).__init__(device, **kwargs)
        # create a layout for this groupbox (to attach widgets on)
        self.device = device
        self.selected = None
        self.view_db = {}
        # register this view in the view list
        self.view_db.setdefault(device, self)
        self.inspector = ParameterView(None)
        self.inspector_device = DeviceInspector(self.device)
        self.layout.addWidget(self.inspector, 0, 0)
        self.layout.addWidget(self.inspector_device, 0, 0)
        self.parameters = QGroupBox('parameters available')
        self.parameters_layout = QGridLayout()
        self.parameters.setLayout(self.parameters_layout)
        self.layout.addWidget(self.parameters, 1, 0)
        self.setup(kwargs)

    def setup(self, kwargs):
        """
        create a Remote for each parameter
        """
        # set title for the DeviceView
        try:
            self.setTitle(self.device.name)
        except:
            self.setTitle(str(self.device))
        # iterate all parameters for this device
        for param in self.device.root_node.get_parameters():
            # create the UI for this parameter
            remote = self.add_remote(param)
            remote.selection_update.connect(self.param_selected)
            self.selection_update.connect(self.device_selected)
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
            self.updater.msgq.register(param)
            # connect the updater thread to this remote
            self.updater.param_update.connect(self.parameter_update)
            # update current state
            remote.new_value(param.value)
            # add the remote to the layout
            self.parameters_layout.addWidget(remote)

    def param_selected(self, parameter):
        """
        a parameter has been selected by clicking inside its groupbox
        """
        # Release last selection
        self.inspector.show()
        self.inspector_device.hide()
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

    def device_selected(self, device):
        """
        a device has been selected by clicking inside its groupbox
        """
        # Release last selection
        self.inspector.hide()
        self.inspector_device.show()
        if self.selected:
            ui = self.view_db[self.selected]
            ui.setStyleSheet("""
                QGroupBox 
                { 
                    border:1px solid rgb(216, 216, 216); 
                }
                """
            )
        self.inspector_device.inspect(device)
        ui = self.view_db[device]
        self.selected = device
        ui = self.view_db[device]
        self.setStyleSheet("""
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
