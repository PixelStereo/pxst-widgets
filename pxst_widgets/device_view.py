#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
A DeviceView represents a bunch of parameters
It is designed to display instruments through remotes
"""

from pxst_widgets.panel import Panel


class DeviceView(Panel):
    """
    PyQt DeviceView that display all params of a device
    float / int : QSlider + QSpiVBox
    string : QLineEdit
    bool : QCheckBox
    todo : tuples : depend of the unit (color, spatial, etc…)
    """
    def __init__(self, *args, **kwargs):
        super(DeviceView, self).__init__()
        # create a layout for this groupbox (to attach widgets on)
        self.device = None
        self.setup(args, kwargs)
        self.resize(args, kwargs)

    def setup(self, args, kwargs):
        """
        create a Remote for each parameter
        """
        if 'device' in kwargs.keys():
            self.device = kwargs['device']
            # set title for the DeviceView
            try:
                self.setTitle(self.device.name)
            except:
                self.setTitle(str(self.device))
            #self.setTitle(str(self.device.get_nodes()[0]))
            for param in self.device.root_node.get_parameters():
                remote = self.add_remote(param)
                self.layout.addWidget(remote)
                remote.setValue(param.value)

    def resize(self, args, kwargs):
        """
        resize the DeviceView from its parameter size
        """
        # set width and height for this device/groupboxs
        if 'height' in kwargs.keys():
            if self.device:
                if kwargs['height'] == 'auto':
                    self.setFixedHeight(len(self.device.root_node.get_parameters()) * 69)
                else:
                    self.setFixedHeight(kwargs['height'])
        if 'height' in kwargs.keys():
            if self.device:
                if kwargs['width'] == 'auto':
                    self.setFixedWidth(305)
                else:
                    self.setFixedWidth(kwargs['width'])
