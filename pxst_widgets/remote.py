#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
pyossia-pyqt module add Graphical User Interface for libossia devices
TODO : create a generic panel with an address attribute
it will automagically display the coreespondant UI for the address
"""

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QPushButton, QGroupBox, QLabel, QHBoxLayout, QSlider, QDial, QLineEdit
from PyQt5.QtGui import QFont


class AbstractValue(QGroupBox):
    """
    PyQt Widget that display label with parameter of the parameter
    float / int : QSlider + QSpinbox
    string : QLineEdit
    bool : QCheckBox
    todo : tuples : depend of the unit (color, spatial, etc…)
    """
    def __init__(self, parameter):
        super(AbstractValue, self).__init__()
        self.parameter = parameter
        # Create label with parameter
        self.label = QLabel(str(self.parameter.node))
        self.label.setFixedSize(100, 20)
        self.label.setFont(QFont('Helvetica', 12, QFont.Light))
        # Create parameter layout
        self.layout = QHBoxLayout()
        self.layout.addWidget(self.label)
        self.setLayout(self.layout)
        #self.setFixedSize(300, 45)
        self.setFixedWidth(300)

    def setValue(self, value):
        """
        Set the value of the GUI
        """
        self.value.setValue(value)

    def new_value(self, new_value):
        """
        check if a new value is there
        """
        if new_value != self.value.value():
            self.parameter_update(new_value)


class TextUI(AbstractValue):
    """

    """
    def __init__(self, parameter):
        super(TextUI, self).__init__(parameter)

    def setValue(self, value):
        """
        Set the value of the GUI
        """
        self.value.setText(value)

    def new_value(self, new_value):
        """
        check if a new value is there
        """
        if new_value != self.value.text():
            self.parameter_update(new_value)

    def parameter_update(self, value):
        self.value.setText(str(value))


class BoolUI(AbstractValue):
    """
    docstring for BoolUI
    """
    def __init__(self, parameter):
        super(BoolUI, self).__init__(parameter)
        self.value = QPushButton(str(self.parameter.value))
        self.value.setCheckable(True)
        self.layout.addWidget(self.value)
        if self.parameter.have_domain():
            ### SOMETHING TO DO
            print('do something please with domain of ' + str(self.parameter))
        self.parameter.add_callback(self.new_value)
        self.value.toggled.connect(self.parameter_push)
        self.value.setChecked(self.parameter.value)

    def parameter_update(self, value):
        self.value.setChecked(value)
        self.value.setText(str(value))

    def parameter_push(self):
        value = self.value.isChecked()
        self.parameter.value = value
        self.value.setText(str(value))

    def setValue(self, value):
        """
        Set the value of the GUI
        """
        self.value.setChecked(value)

    def new_value(self, new_value):
        """
        check if a new value is there
        """
        if new_value != self.value.isChecked():
            self.parameter_update(new_value)

class IntUI(AbstractValue):
    """
    docstring for FloatUI
    """
    def __init__(self, parameter):
        super(IntUI, self).__init__(parameter)
        self.value = QSlider(Qt.Horizontal, None)
        self.layout.addWidget(self.value)
        if self.parameter.have_domain():
            self.value.setRange(self.parameter.domain.min, self.parameter.domain.max)
        else:
            self.value.setRange(0, 100)
        self.parameter.add_callback(self.new_value)
        self.value.valueChanged.connect(self.parameter.push_value)

    def parameter_update(self, value):
        self.value.setValue(value)


class FloatUI(AbstractValue):
    """
    docstring for FloatUI
    """
    def __init__(self, parameter):
        super(FloatUI, self).__init__(parameter)
        self.value = QSlider(Qt.Horizontal, None)
        self.layout.addWidget(self.value)
        if self.parameter.have_domain():
            range_min = self.parameter.domain.min*32768
            range_max = self.parameter.domain.max*32768
            self.value.setRange(range_min, range_max)
        else:
            self.value.setRange(0, 32768)
        def parameter_push(value):
            value = float(value/32768)
            self.parameter.value = value
        self.parameter.add_callback(self.new_value)
        self.value.valueChanged.connect(parameter_push)

    def parameter_update(self, value):
        value = value*32768
        self.value.setValue(value)

class Vec2fUI(AbstractValue):
    """
    docstring for Vec3f
    """
    def __init__(self, parameter):
        super(Vec2fUI, self).__init__(parameter)
        self.value1 = QDial()
        self.value2 = QDial()
        self.value1.setValue(1)
        self.value2.setValue(1)
        self.value1.setFixedSize(35, 35)
        self.value2.setFixedSize(35, 35)
        self.value1.setRange(0, 32768)
        self.value2.setRange(0, 32768)
        def parameter_push():
            value_1 = round(self.value1.value()/32768, 4)
            value_2 = round(self.value2.value()/32768, 4)
            self.parameter.value = [value_1, value_2]
        self.value1.valueChanged.connect(parameter_push)
        self.value2.valueChanged.connect(parameter_push)
        self.layout.addWidget(self.value1)
        self.layout.addWidget(self.value2)
        if self.parameter.have_domain():
            ### SOMETHING TO DO
            print('do something please with domain of ' + str(self.parameter))
        self.parameter.add_callback(self.new_value)

    def parameter_update(self, value):
        print('------UPDATE-------', value)
        value1 = int(value[0]*32768)
        value2 = int(value[1]*32768)
        self.setValue([value1, value2])

    def setValue(self, value):
        """
        Set the value of the GUI
        """
        self.value1.setValue(value[0])
        self.value2.setValue(value[1])

    def new_value(self, new_value):
        """
        check if a new value is there
        """
        new_value1 = int(new_value[0]*32768)
        new_value2 = int(new_value[1]*32768)
        print(1, new_value1, self.value1.value())
        print(2, new_value2, self.value2.value())
        if new_value1 != self.value1.value():
            self.value1.setValue(new_value1)
        if new_value2 != self.value2.value():
            print(222222)
            self.value2.setValue(new_value2)
        print(333333)


class Vec3fUI(AbstractValue):
    """
    docstring for Vec3f
    """
    def __init__(self, parameter):
        super(Vec3fUI, self).__init__(parameter)
        self.value1 = QDial()
        self.value2 = QDial()
        self.value3 = QDial()
        self.value1.setValue(1)
        self.value2.setValue(1)
        self.value3.setValue(1)
        self.value1.setFixedSize(35, 35)
        self.value2.setFixedSize(35, 35)
        self.value3.setFixedSize(35, 35)
        self.value1.setRange(0, 32768)
        self.value2.setRange(0, 32768)
        self.value3.setRange(0, 32768)
        def parameter_push():
            value_1 = self.value1.value()/32768
            value_2 = self.value2.value()/32768
            value_3 = self.value3.value()/32768
            self.parameter.value = [value_1, value_2, value_3]
        self.value1.valueChanged.connect(parameter_push)
        self.value2.valueChanged.connect(parameter_push)
        self.value3.valueChanged.connect(parameter_push)
        self.layout.addWidget(self.value1)
        self.layout.addWidget(self.value2)
        self.layout.addWidget(self.value3)
        if self.parameter.have_domain():
            ### SOMETHING TO DO
            print('do something please with domain of ' + str(self.parameter))
        self.parameter.add_callback(self.new_value)

    def parameter_update(self, value):
        value1 = int(value[0]*32768)
        value2 = int(value[1]*32768)
        value3 = int(value[2]*32768)
        self.setValue([value1, value2, value3])

    def setValue(self, value):
        """
        Set the value of the GUI
        """
        self.value1.setValue(value[0])
        self.value2.setValue(value[1])
        self.value3.setValue(value[2])

    def new_value(self, new_value):
        """
        check if a new value is there
        """
        new_value1 = int(new_value[0]*32768)
        new_value2 = int(new_value[1]*32768)
        new_value3 = int(new_value[2]*32768)
        if new_value1 != self.value1.value():
            self.value1.setValue(new_value2)
        if new_value2 != self.value2.value():
            self.value2.setValue(new_value2)
        if new_value3 != self.value3.value():
            self.value3.setValue(new_value3)


class Vec4fUI(AbstractValue):
    """
    docstring for Vec3f
    """
    def __init__(self, parameter):
        super(Vec4fUI, self).__init__(parameter)
        self.value1 = QDial()
        self.value2 = QDial()
        self.value3 = QDial()
        self.value4 = QDial()
        self.value1.setValue(1)
        self.value2.setValue(1)
        self.value3.setValue(1)
        self.value4.setValue(1)
        self.value1.setFixedSize(35, 35)
        self.value2.setFixedSize(35, 35)
        self.value3.setFixedSize(35, 35)
        self.value4.setFixedSize(35, 35)
        self.value1.setRange(0, 32768)
        self.value2.setRange(0, 32768)
        self.value3.setRange(0, 32768)
        self.value4.setRange(0, 32768)
        def parameter_push():
            value_1 = self.value1.value()/32768
            value_2 = self.value2.value()/32768
            value_3 = self.value3.value()/32768
            value_4 = self.value4.value()/32768
            self.parameter.value = [value_1, value_2, value_3, value_4]
        self.value1.valueChanged.connect(parameter_push)
        self.value2.valueChanged.connect(parameter_push)
        self.value3.valueChanged.connect(parameter_push)
        self.value4.valueChanged.connect(parameter_push)
        self.layout.addWidget(self.value1)
        self.layout.addWidget(self.value2)
        self.layout.addWidget(self.value3)
        self.layout.addWidget(self.value4)
        if self.parameter.have_domain():
            ### SOMETHING TO DO
            print('do something please with domain of ' + str(self.parameter))
        self.parameter.add_callback(self.new_value)

    def parameter_update(self, value):
        value1 = int(value[0]*32768)
        value2 = int(value[1]*32768)
        value3 = int(value[2]*32768)
        value4 = int(value[3]*32768)
        self.setValue([value1, value2, value3, value4])

    def setValue(self, value):
        """
        Set the value of the GUI
        """
        self.value1.setValue(value[0])
        self.value2.setValue(value[1])
        self.value3.setValue(value[2])
        self.value4.setValue(value[3])

    def new_value(self, new_value):
        """
        check if a new value is there
        """
        new_value1 = int(new_value[0]*32768)
        new_value2 = int(new_value[1]*32768)
        new_value3 = int(new_value[2]*32768)
        new_value4 = int(new_value[3]*32768)
        if new_value1 != self.value1.value():
            self.value1.setValue(new_value2)
        if new_value2 != self.value2.value():
            self.value2.setValue(new_value2)
        if new_value3 != self.value3.value():
            self.value3.setValue(new_value3)
        if new_value4 != self.value4.value():
            self.value4.setValue(new_value4)


class CharUI(TextUI):
    """
    docstring for StringUI
    """
    def __init__(self, parameter):
        super(CharUI, self).__init__(parameter)
        self.value = QLineEdit()
        self.value.setAttribute(Qt.WA_MacShowFocusRect, 0)
        self.layout.addWidget(self.value)
        if self.parameter.have_domain():
            ### SOMETHING TO DO
            print('do something please with domain of ' + str(self.parameter))
        self.value.textEdited.connect(self.parameter.push_value)
        self.parameter.add_callback(self.new_value)

    def parameter_update(self, value):
        # TODO : please format is as a chat
        self.value.setText(str(value))


class ListUI(TextUI):
    """
    docstring for StringUI
    """
    def __init__(self, parameter):
        super(ListUI, self).__init__(parameter)
        self.value = QLineEdit()
        self.value.setAttribute(Qt.WA_MacShowFocusRect, 0)
        self.layout.addWidget(self.value)
        if self.parameter.have_domain():
            ### SOMETHING TO DO
            print('do something please with domain of ' + str(self.parameter))
        def parameter_push(value):
            value = value.split(' ')
            self.parameter.value = value
        self.value.textEdited.connect(parameter_push)
        self.parameter.add_callback(self.new_value)

    def parameter_update(self, value):
        display = ''.join(str(e) for e in value)
        # TODO : please remove brackets from list her
        self.value.setText(", ".join(value))

    def setValue(self, value):
        """
        Set the value of the GUI
        """
        self.value.setText(str(value))



class StringUI(TextUI):
    """
    docstring for StringUI
    """
    def __init__(self, parameter):
        super(StringUI, self).__init__(parameter)
        self.value = QLineEdit()
        self.value.setAttribute(Qt.WA_MacShowFocusRect, 0)
        self.layout.addWidget(self.value)
        if self.parameter.have_domain():
            ### SOMETHING TO DO
            print('do something please with domain of ' + str(self.parameter))
        self.value.textEdited.connect(self.parameter.push_value)
        self.parameter.add_callback(self.new_value)

