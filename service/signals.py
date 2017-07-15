#!/usr/bin/python3
# -*- coding: utf-8 -*-

from PyQt5.QtCore import pyqtSignal, QObject

__author__ = 'Bartosz Kościow'


class StreamSignal(QObject):
    state = pyqtSignal(str)


SIGNALS = {
    'stream': StreamSignal(),
}
