#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
A Panel is a Group of widget designed to add Parameter remotes
"""

from PyQt5.QtWidgets import QGroupBox, QGridLayout
from PyQt5.QtCore import pyqtSignal
from pyossia import ossia
from pxst_widgets.inspector import NodeView, ParameterView
from pxst_widgets.remote import Vec3fUI, Vec4fUI, ListUI, CharUI, ImpulseUI
from pxst_widgets.remote import FloatUI, BoolUI, IntUI, StringUI, Vec2fUI
from pxst_widgets.device_queue import DeviceQueue

class Panel(QGroupBox):
    """
    A QGroupBox to put one or several remote inside
    """
    selection_update = pyqtSignal(ossia.LocalDevice)
    def __init__(self, *args, **kwargs):
        super(Panel, self).__init__()
        # create a layout for this groupbox (to attach widgets on)
        self.layout = QGridLayout()
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self._device = None
        if len(args) > 0:
            self.device = args[0]
        self.setLayout(self.layout)

    def mousePressEvent(self, event):
        """
        This is used to know if the remote UI has been Clicked
        """
        if self.device:
            self.selection_update.emit(self.device)
        event.accept()

    def add_remote(self, parameter):
        """
        Add a QWidget for the current Value
        """
        if parameter.value_type == ossia.ValueType.Float:
            remote = FloatUI(parameter)
        elif parameter.value_type == ossia.ValueType.Bool:
            remote = BoolUI(parameter)
        elif parameter.value_type == ossia.ValueType.Int:
            remote = IntUI(parameter)
        elif parameter.value_type == ossia.ValueType.String:
            remote = StringUI(parameter)
        elif parameter.value_type == ossia.ValueType.Vec2f:
            remote = Vec2fUI(parameter)
        elif parameter.value_type == ossia.ValueType.Vec3f:
            remote = Vec3fUI(parameter)
        elif parameter.value_type == ossia.ValueType.Vec4f:
            remote = Vec4fUI(parameter)
        elif parameter.value_type == ossia.ValueType.List:
            remote = ListUI(parameter)
        elif parameter.value_type == ossia.ValueType.Char:
            remote = CharUI(parameter)
        elif parameter.value_type == ossia.ValueType.Impulse:
            remote = ImpulseUI(parameter)
        else:
            print('ERROR 999', parameter.value_type)
            remote = StringUI(parameter)
        self.layout.addWidget(remote, 1, 1)
        return remote


    def add_inspector(self, node_or_param_to_inspect):
        if node_or_param_to_inspect.__class__.__name__ == 'Node':
            inspector = NodeView(node_or_param_to_inspect)
        elif node_or_param_to_inspect.__class__.__name__ == 'Parameter':
            inspector = ParameterView(node_or_param_to_inspect)
        self.layout.addWidget(inspector, 1, 1)
        return inspector

    @property
    def device(self):
        return self._device
    @device.setter
    def device(self, device):
        if device:
            self._device = device
            # create a messageQueue for this Device
            self.updater = DeviceQueue(self, device)
