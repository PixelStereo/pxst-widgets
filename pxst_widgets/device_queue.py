#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
A DeviceQueue runs in a separate thrad for an ossia device.
It emt a signal when a new value is in the queue
"""

from pyossia import ossia
from PyQt5.Qt import QThread, pyqtSignal


class DeviceQueue(QThread):
    """
    Run a Device update queue
    """
    param_update = pyqtSignal(ossia.Parameter, object)
    def __init__(self, parent):
        super(DeviceQueue, self).__init__()
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
