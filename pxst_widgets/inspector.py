#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
An Inspector is a graphical user interface that displays 
all attributes or a device, a node or a parameter.
"""

from PyQt5.QtWidgets import QGroupBox, QGridLayout, QLineEdit, QLabel


class NodeView(QGroupBox):
    """
    Base class for Inspecter Widgets
    """
    def __init__(self, node):
        super(NodeView, self).__init__()
        self.layout = QGridLayout()
        self.setLayout(self.layout)
        self.setup()
        self.setMinimumWidth(300)
        self.inspect(node)

    def setup(self):

        # value
        # description
        self.description_label = QLabel('description')
        self.layout.addWidget(self.description_label, 0, 0)
        self.description = QLineEdit()
        self.layout.addWidget(self.description, 0, 1)        

        # critical
        self.critical_label = QLabel('critical')
        self.layout.addWidget(self.critical_label, 1, 0)
        self.critical = QLineEdit()
        self.layout.addWidget(self.critical, 1, 1)

        # tags
        self.tags_label = QLabel('tags')
        self.layout.addWidget(self.tags_label, 2, 0)
        self.tags = QLineEdit()
        self.layout.addWidget(self.tags, 2, 1)

    def inspect(self, node):
        self.node = node
        # address
        self.setTitle(str(node))
        # description
        self.description.setText(self.node.description)

        # critical
        self.critical.setText(str(self.node.critical))

        # tags
        self.tags.setText(str(self.node.tags))


class ParameterView(QGroupBox):
    """
    Base class for Inspecter Widgets
    """
    def __init__(self, parameter):
        super(ParameterView, self).__init__()
        self.layout = QGridLayout()
        self.setLayout(self.layout)
        self.setup()
        self.setMinimumWidth(300)

        if parameter:
            self.parameter = parameter
            self.inspect(parameter)
        else:
            self.setTitle('select a parameter to inspect')

    def setup(self):

        # value
        # description
        self.description_label = QLabel('description')
        self.layout.addWidget(self.description_label, 0, 0)
        self.description = QLineEdit()
        self.layout.addWidget(self.description, 0, 1)        

        # value_type
        self.value_type_label = QLabel('value_type')
        self.layout.addWidget(self.value_type_label, 1, 0)
        self.value_type = QLineEdit()
        self.layout.addWidget(self.value_type, 1, 1)

        # default_value
        self.default_value_label = QLabel('default_value')
        self.layout.addWidget(self.default_value_label, 2, 0)
        self.default_value = QLineEdit()
        self.layout.addWidget(self.default_value, 2, 1)

        # domain
        self.domain_label = QLabel('domain')
        self.layout.addWidget(self.domain_label, 4, 0)
        self.domain = QLineEdit()
        self.layout.addWidget(self.domain, 4, 1)

        # unit
        self.unit_label = QLabel('unit')
        self.layout.addWidget(self.unit_label, 5, 0)
        self.unit = QLineEdit()
        self.layout.addWidget(self.unit, 5, 1)

        # boudning_mode
        self.bounding_mode_label = QLabel('bounding_mode')
        self.layout.addWidget(self.bounding_mode_label, 6, 0)
        self.bounding_mode = QLineEdit()
        self.layout.addWidget(self.bounding_mode, 6, 1)

        # repetition_filter
        self.repetition_filter_label = QLabel('repetition_filter')
        self.layout.addWidget(self.repetition_filter_label, 7, 0)
        self.repetition_filter = QLineEdit()
        self.layout.addWidget(self.repetition_filter, 7, 1)

        # critical
        self.critical_label = QLabel('critical')
        self.layout.addWidget(self.critical_label, 8, 0)
        self.critical = QLineEdit()
        self.layout.addWidget(self.critical, 8, 1)

        # tags
        self.tags_label = QLabel('tags')
        self.layout.addWidget(self.tags_label, 9, 0)
        self.tags = QLineEdit()
        self.layout.addWidget(self.tags, 9, 1)

    def inspect(self, parameter):
        self.parameter = parameter
        # address
        self.setTitle(str(parameter.node))
        # description
        self.description.setText(self.parameter.node.description)

        # value_type
        self.value_type.setText(str(self.parameter.value_type))

        # default_value
        self.default_value.setText(str(self.parameter.default_value))

        # domain
        self.domain.setText(str(self.parameter.domain.min) + ' ' + str(self.parameter.domain.max))

        # bounding_mode
        self.bounding_mode.setText(str(self.parameter.bounding_mode))

        # repetition_filter
        self.repetition_filter.setText(str(self.parameter.repetition_filter))

        # unit
        self.unit.setText(str(self.parameter.unit))

        # critical
        self.critical.setText(str(self.parameter.node.critical))

        # tags
        self.tags.setText(str(self.parameter.node.tags))

class DeviceInspector(QGroupBox):
    """
    Base class for Inspecter Widgets
    """
    def __init__(self, device):
        super(DeviceInspector, self).__init__()
        self.layout = QGridLayout()
        self.setLayout(self.layout)
        self.setup()
        self.setMinimumWidth(300)
        self.device = device

        if device:
            self.inspect(device)
        else:
            self.setTitle('select a device to inspect')
        self.hide()

    def setup(self):

        # value
        # description
        self.root_node_label = QLabel('root_node')
        self.layout.addWidget(self.root_node_label, 0, 0)
        self.root_node = QLineEdit()
        self.layout.addWidget(self.root_node, 0, 1)        

    def inspect(self, device):
        self.device = device
        # address
        self.setTitle(str(self.device.name))
        # description
        self.root_node.setText(str(self.device.root_node))
