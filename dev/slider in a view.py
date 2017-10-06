#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
longqi 21/Jan/16 14:35

"""

from PyQt5 import QtGui, QtCore, Qt
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *



class SpinBoxDelegate(QItemDelegate):
    def createEditor(self, parent, option, index):
        editor = QSlider(parent, orientation=Qt.Horizontal)
        editor.setMinimum(0)
        editor.setMaximum(100)

        return editor

    def setEditorData(self, slider, index):
        value = index.model().data(index, Qt.EditRole)

        slider.setValue(value)

    def setModelData(self, slider, model, index):
        value = slider.value()
        model.setData(index, value, Qt.EditRole)

    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)


if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)

    model = QStandardItemModel(4, 2)
    tableView = QTableView()
    tableView.setModel(model)

    delegate = SpinBoxDelegate()
    tableView.setItemDelegate(delegate)

    for row in range(4):
        for column in range(2):
            index = model.index(row, column, QModelIndex())
            model.setData(index, (row + 1) * (column + 1))

    tableView.setWindowTitle("Spin Box Delegate")
    tableView.show()
    sys.exit(app.exec_())
