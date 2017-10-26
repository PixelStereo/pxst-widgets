#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
An Inspector is a graphical user interface that displays 
all attributes or a device, a node or a parameter.
"""

from PyQt5.QtWidgets import QGroupBox, QGridLayout, QLineEdit, QLabel

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

        # boudning_mode
        self.bounding_mode_label = QLabel('bounding_mode')
        self.layout.addWidget(self.bounding_mode_label, 5, 0)
        self.bounding_mode = QLineEdit()
        self.layout.addWidget(self.bounding_mode, 5, 1)

        # repetition_filter
        self.repetition_filter_label = QLabel('repetition_filter')
        self.layout.addWidget(self.repetition_filter_label, 6, 0)
        self.repetition_filter = QLineEdit()
        self.layout.addWidget(self.repetition_filter, 6, 1)


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
