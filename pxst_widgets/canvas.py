#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
A Canvas represents 
"""

from pyossia import *
from pxst_widgets.valueUI import *

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QGroupBox, QVBoxLayout
from PyQt5.QtGui import QFont

######################################################
# Module Constants
######################################################

######################################################
# Module functions / shortcuts to create GUI
######################################################

class Canvas(QGroupBox):
    """
    PyQt Canvas that display all params of a device
    float / int : QSlider + QSpiVBox
    string : QLineEdit
    bool : QCheckBox
    todo : tuples : depend of the unit (color, spatial, etc…)
    """
    def __init__(self,  *args, **kwargs):
        super(Canvas, self).__init__()
        # create a layout for this groupbox (to attach widgets on)
        self.layout = QVBoxLayout()
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0);
        self.device = None
        self.setLayout(self.layout)
        if 'device' in kwargs.keys():
            self.device = kwargs['device']
            # set title for the 
            self.setTitle(str(self.device))
            #self.setTitle(str(self.device.get_nodes()[0]))
            for param in self.device.get_parameters():
                paramUI = self.add_ValueUI(param.address)
                self.layout.addWidget(paramUI)
        # set width and height for this device/groupboxs
        if 'height' in kwargs.keys():
            if self.device:
                if kwargs['height'] == 'auto':
                    self.setFixedHeight(len(self.device.get_parameters()) * 49)
                else:
                    self.setFixedHeight(kwargs['height'])
        if 'height' in kwargs.keys():
                if kwargs['width'] == 'auto':
                    self.setFixedWidth(305)
                else:
                    self.setFixedWidth(kwargs['width'])


    def add_ValueUI(self, ossia_parameter):
        """
        Add a QWidget for the current Value
        """
        if ossia_parameter.value_type == ossia.ValueType.Float:
            paramUI = FloatUI(ossia_parameter)
        elif ossia_parameter.value_type == ossia.ValueType.Bool:
            paramUI = BoolUI(ossia_parameter)
        elif ossia_parameter.value_type == ossia.ValueType.Int:
            paramUI = IntUI(ossia_parameter)
        elif ossia_parameter.value_type == ossia.ValueType.String:
            paramUI = StringUI(ossia_parameter)
        elif ossia_parameter.value_type == ossia.ValueType.Vec3f:
            paramUI = StringUI(ossia_parameter)
        elif ossia_parameter.value_type == ossia.ValueType.List:
            paramUI = StringUI(ossia_parameter)
        return paramUI
