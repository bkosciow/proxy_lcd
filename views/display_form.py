#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author__ = 'Bartosz Kościów'
from PyQt5.QtWidgets import QDialog, QGridLayout, QLabel, QLineEdit, QCheckBox, \
    QDialogButtonBox, QComboBox, QVBoxLayout, QHBoxLayout
from PyQt5.QtCore import Qt
from charlcd.drivers.wifi_content import WiFi
from charlcd.buffered import CharLCD
from model.display import Display
from PyQt5.QtGui import QIcon


class DisplayForm(QDialog):
    def __init__(self, msg, broadcast_ip, broadcast_port, display=None, parent=None):
        super().__init__(parent)
        self.msg = msg
        self.broadcast_ip = broadcast_ip
        self.broadcast_port = broadcast_port
        self.widgets = {}
        self.init_gui()

        self.setWindowTitle('Add display')
        self.display = display
        if display is not None:
            self.fill_data(display)

    def init_gui(self):
        """display GUI"""
        self.setWindowIcon(QIcon('img/icon.png'))
        layout = QGridLayout(self)

        name_label = QLabel('Name')
        name = QLineEdit()
        layout.addWidget(name_label, 1, 0)
        layout.addWidget(name, 1, 1, 1, 2)
        self.widgets['name'] = name

        node_name_label = QLabel('Node name')
        node_name = QLineEdit()
        layout.addWidget(node_name_label, 2, 0)
        layout.addWidget(node_name, 2, 1, 1, 2)
        self.widgets['node_name'] = node_name

        size_label = QLabel('Size (w*h)')
        size_x = QLineEdit()
        size_y = QLineEdit()
        size_x.setMaximumWidth(40)
        size_y.setMaximumWidth(40)
        layout.addWidget(size_label, 3, 0)
        layout.addWidget(size_x, 3, 1)
        layout.addWidget(size_y, 3, 2)
        self.widgets['size'] = {
            'x': size_x,
            'y': size_y
        }

        stream_label = QLabel('Stream')
        stream = QCheckBox()
        layout.addWidget(stream_label, 4, 0)
        layout.addWidget(stream, 4, 1, 1, 2)
        self.widgets['stream'] = stream

        formatter_label = QLabel('Formatter')
        formatter = QComboBox()
        # items = self.fo
        # size.addItem('16x2')
        # size.addItem('20x4')
        # size.addItem('40x4')
        layout.addWidget(formatter_label, 5, 0)

        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
            Qt.Horizontal, self)
        layout.addWidget(buttons, 6, 0, 1, 3)

        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

    def fill_data(self, display):
        """fill form with data from Display"""
        self.widgets['node_name'].setText(display.node_name)
        self.widgets['name'].setText(display.name)
        self.widgets['stream'].setChecked(True if display.can_stream else False)
        size = display.get_size()
        self.widgets['size']['x'].setText(str(size[0]))
        self.widgets['size']['y'].setText(str(size[1]))

    def get_display(self):
        """rturns Display object"""
        drv = WiFi(self.msg, [self.widgets['node_name'].text()], (self.broadcast_ip, self.broadcast_port))
        lcd = CharLCD(
            int(
                self.widgets['size']['x'].text()),
            int(
                self.widgets['size']['y'].text()),
            drv)
        lcd.init()

        return Display(
            self.display.uuid if self.display else None,
            self.widgets['name'].text(),
            lcd,
            self.widgets['stream'].isChecked(),
            'charlcd',
            'clean'
        )

