#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
pyossia-pyqt module add Graphical User Interface for libossia devices
TODO : create a generic panel with an address attribute
it will automagically display the coreespondant UI for the address
"""

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QPushButton, QGroupBox, QLabel, QGridLayout, QSlider, QDial, QLineEdit
from PyQt5.QtGui import QFont
from pyossia import ossia


class AbstractValueUI(QGroupBox):
    """
    This must be sublassed with a value attribute set to a UI widget / object
    PyQt Widget that display label with parameter of the parameter
    """
    selection_update = pyqtSignal(ossia.Parameter)
    def __init__(self, parameter):
        super(AbstractValueUI, self).__init__()
        self.parameter = parameter
        # Create parameter layout
        self.layout = QGridLayout()
        # create a button to reset the parameter to its default_value
        self.reset_ui = QPushButton('reset')
        self.reset_ui.setFixedSize(100, 20)
        #self.reset_ui.setFont(QFont('Helvetica', 9, QFont.Light))
        #self.reset_ui.toggled.connect(self.parameter.reset)
        self.reset_ui.setCheckable(False)
        self.reset_ui.setFlat(True)
        self.reset_ui.clicked.connect(self.parameter.reset)
        self.layout.addWidget(self.reset_ui, 0, 0, 1, 3)
        # Create label with parameter
        self.label = QLabel(str(self.parameter.node))
        self.label.setFixedSize(100, 20)
        self.label.setFont(QFont('Helvetica', 12, QFont.Light))
        self.layout.addWidget(self.label, 0, 4, 1, 3)
        self.setLayout(self.layout)
        #self.setFixedSize(300, 45)
        self.setFixedWidth(300)

    def mousePressEvent(self, event):
        """
        This is used to know if the remote UI has been Clicked
        """
        self.selection_update.emit(self.parameter)

    def mute(self, state):
        """
        mechanism used to avoid infinite loop when setting an UI
        """
        self.value.blockSignals(state)
        if state:
            self.value.setUpdatesEnabled(False)
        else:
            self.value.setUpdatesEnabled(True)

    def new_value(self, value):
        """
        check if a new value is there
        """
        if value != self.getUI():
            # this is a new value, please set the UI
            # block signal from new value
            self.mute(True)
            self.setUI(value)
            self.mute(False)


class ImpulseUI(AbstractValueUI):
    """
    Widget for an Impulse Parameter
    """
    def __init__(self, parameter):
        super(ImpulseUI, self).__init__(parameter)
        self.value = QPushButton(str(parameter.node))
        self.value.setCheckable(False)
        self.value.setFlat(True)
        self.layout.addWidget(self.value)
        self.value.toggled.connect(self.parameter.push_value)

    def setUI(self, value):
        self.value.setChecked(False)

    def getUI(self):
        return False


class IntUI(AbstractValueUI):
    """
    docstring for FloatUI
    """
    def __init__(self, parameter):
        super(IntUI, self).__init__(parameter)
        self.value = QSlider(Qt.Horizontal, None)
        self.layout.addWidget(self.value)
        if self.parameter.have_domain():
            if self.parameter.domain.min and self.parameter.domain.max:
                self.value.setRange(self.parameter.domain.min, self.parameter.domain.max)
            else:
                self.value.setRange(0, 100)
        else:
            self.value.setRange(0, 100)
        self.value.valueChanged.connect(self.parameter.push_value)

    def setUI(self, value):
        self.value.setSliderPosition(value)

    def getUI(self):
        return self.value.sliderPosition()


class FloatUI(AbstractValueUI):
    """
    docstring for FloatUI
    """
    def __init__(self, parameter):
        super(FloatUI, self).__init__(parameter)
        self.value = QSlider(Qt.Horizontal, None)
        self.layout.addWidget(self.value)
        if self.parameter.have_domain():
            if self.parameter.domain.min:
                range_min = self.parameter.domain.min*32768
            else:
                range_min = 0
            if self.parameter.domain.max:
                range_max = self.parameter.domain.max*32768
            else:
                range_max = 32768
            self.value.setRange(range_min, range_max)
        else:
            self.value.setRange(0, 32768)
        def parameter_push(value):
            value = float(value/32768)
            self.parameter.push_value(value)
        self.value.valueChanged.connect(parameter_push)

    def setUI(self, value):
        self.value.setSliderPosition(value*32768)

    def getUI(self):
        return self.value.sliderPosition()/32768

class BoolUI(AbstractValueUI):
    """
    docstring for BoolUI
    """
    def __init__(self, parameter):
        super(BoolUI, self).__init__(parameter)
        self.value = QPushButton(str(self.parameter.value))
        self.value.setCheckable(True)
        self.value.setFlat(True)
        self.value.toggled.connect(lambda value: self.value.setText(str(value)))
        self.layout.addWidget(self.value)
        self.value.toggled.connect(self.parameter.push_value)

    def setUI(self, value):
        self.value.setChecked(value)
        self.value.setText(str(value))

    def getUI(self):
        return self.value.isChecked()


class TextUI(AbstractValueUI):
    """
    This is a base class for Text Based UI
    """
    def __init__(self, parameter):
        super(TextUI, self).__init__(parameter)
        self.value = QLineEdit()
        self.value.setAttribute(Qt.WA_MacShowFocusRect, 0)
        self.layout.addWidget(self.value)
        if self.parameter.have_domain():
            ### SOMETHING TO DO
            print('TODO : domain of string based parameter : ' + str(self.parameter))

    def setUI(self, value):
        self.value.setText(str(value))

    def getUI(self):
        return self.value.text()


class CharUI(TextUI):
    """
    The CharUI is a Text based UI for a single Ascii Character
    """
    def __init__(self, parameter):
        super(CharUI, self).__init__(parameter)
        self.value.textEdited.connect(self.parameter.push_value)


class ListUI(TextUI):
    """
    The List is a Text based UI that display a List as a string
    """
    def __init__(self, parameter):
        super(ListUI, self).__init__(parameter)
        def parameter_push(value):
            """
            Dedicated fonction to format list from a QLine Edit to Ossia Pusher
            """
            # remove brackets (first and last characters of the string)
            if len(value) >3:
                value = value[1:-1]
            # split the string in items
            value = value.split(', ')
            print(type(value), value)
            for val in value:
                print(type(val), val)
            self.parameter.push_value(value)
        self.value.textEdited.connect(parameter_push)

        def setUI(self, value):
            self.value.setText(value)


class StringUI(TextUI):
    """
    The String is a Text based UI that display a string
    """
    def __init__(self, parameter):
        super(StringUI, self).__init__(parameter)
        self.value.textEdited.connect(self.parameter.push_value)


class Vec2fUI(AbstractValueUI):
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
            value_1 = self.value1.value()/32768
            value_2 = self.value2.value()/32768
            self.parameter.value = [value_1, value_2]
        self.value1.valueChanged.connect(parameter_push)
        self.value2.valueChanged.connect(parameter_push)
        self.layout.addWidget(self.value1)
        self.layout.addWidget(self.value2)
        if self.parameter.have_domain():
            print(self.parameter.domain.min, self.parameter.domain.min)

    def setUI(self, value):
        """
        Set the value of the GUI
        """
        self.value1.setValue(value[0]*32768)
        self.value2.setValue(value[1]*32768)

    def getUI(self):
        """
        Set the value of the GUI
        """
        return [self.value1.value()/32768, self.value2.value()/32768]

    def mute(self, state):
        """
        mechanism used to avoid infinite loop when setting an UI
        """
        self.value1.blockSignals(state)
        self.value2.blockSignals(state)
        if state:
            self.value1.setUpdatesEnabled(False)
            self.value2.setUpdatesEnabled(False)
        else:
            self.value1.setUpdatesEnabled(True)
            self.value2.setUpdatesEnabled(True)


class Vec3fUI(AbstractValueUI):
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
        self.layout.addWidget(self.value1, 1, 0)
        self.layout.addWidget(self.value2, 1, 1)
        self.layout.addWidget(self.value3, 1, 2)

    def setUI(self, value):
        """
        Set the value of the GUI
        """
        self.value1.setValue(value[0]*32768)
        self.value2.setValue(value[1]*32768)
        self.value3.setValue(value[2]*32768)

    def getUI(self):
        """
        Set the value of the GUI
        """
        return [self.value1.value()/32768, self.value2.value()/32768, self.value3.value()/32768]

    def mute(self, state):
        """
        mechanism used to avoid infinite loop when setting an UI
        """
        self.value1.blockSignals(state)
        self.value2.blockSignals(state)
        self.value3.blockSignals(state)
        if state:
            self.value1.setUpdatesEnabled(False)
            self.value2.setUpdatesEnabled(False)
            self.value3.setUpdatesEnabled(False)
        else:
            self.value1.setUpdatesEnabled(True)
            self.value2.setUpdatesEnabled(True)
            self.value3.setUpdatesEnabled(True)


class Vec4fUI(AbstractValueUI):
    """
    docstring for Vec4f
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
        self.layout.addWidget(self.value1, 1, 0, 1, 2)
        self.layout.addWidget(self.value2, 1, 4, 1, 2)
        self.layout.addWidget(self.value3, 1, 8, 1, 2)
        self.layout.addWidget(self.value4, 1, 12, 1, 2)

    def setUI(self, value):
        """
        Set the value of the GUI
        """
        self.value1.setValue(value[0]*32768)
        self.value2.setValue(value[1]*32768)
        self.value3.setValue(value[2]*32768)
        self.value4.setValue(value[3]*32768)

    def getUI(self):
        """
        Set the value of the GUI
        """
        return [self.value1.value()/32768, self.value2.value()/32768, self.value3.value()/32768, self.value4.value()/32768]

    def mute(self, state):
        """
        mechanism used to avoid infinite loop when setting an UI
        """
        self.value1.blockSignals(state)
        self.value2.blockSignals(state)
        self.value3.blockSignals(state)
        self.value4.blockSignals(state)
        if state:
            self.value1.setUpdatesEnabled(False)
            self.value2.setUpdatesEnabled(False)
            self.value3.setUpdatesEnabled(False)
            self.value4.setUpdatesEnabled(False)
        else:
            self.value1.setUpdatesEnabled(True)
            self.value2.setUpdatesEnabled(True)
            self.value3.setUpdatesEnabled(True)
            self.value4.setUpdatesEnabled(True)
