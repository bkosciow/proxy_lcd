#!/usr/bin/python3
# -*- coding: utf-8 -*-

from PyQt5.QtGui import QIcon
from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMessageBox, QMainWindow, QAction, qApp, QVBoxLayout, \
    QWidget, QTableWidget, QTableWidgetItem
from views.display_form import DisplayForm


class MainView(QMainWindow):
    """Main window"""
    def __init__(self, lcd_repository):
        super().__init__()
        self.lcd_repository = lcd_repository
        self.widgets = {
            'table_widget': None
        }
        self.table_widget = None
        self._init_menu()
        self._init_gui()
        self._init_content(self.widgets['hbox'])

    def _init_gui(self):
        """prepare main widget and attach layout"""
        self.setWindowIcon(QIcon('img/icon.png'))
        widget = QWidget()
        self.setCentralWidget(widget)
        hbox = QVBoxLayout()
        hbox.setAlignment(Qt.AlignTop)

        self.widgets['hbox'] = hbox
        widget.setLayout(hbox)
        self.resize(640, 400)
        self.setWindowTitle('Proxy LCD')
        self.show()

    def _init_menu(self):
        """preapre manu and menubar"""
        exit_action = QAction(QIcon('img/exit.png'), '&Exit', self)
        exit_action.triggered.connect(qApp.quit)

        add_action = QAction(QIcon('img/add.png'), '&Add', self)
        add_action.triggered.connect(self._add_action)

        delete_action = QAction(QIcon('img/delete.png'), '&Delete', self)
        delete_action.triggered.connect(self._delete_action)
        delete_action.setDisabled(True)
        self.widgets['delete_action'] = delete_action

        edit_action = QAction(QIcon('img/edit.png'), '&Edit', self)
        edit_action.triggered.connect(self._edit_action)
        edit_action.setDisabled(True)
        self.widgets['edit_action'] = edit_action

        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu('&File')
        file_menu.addAction(exit_action)

        display_menu = menu_bar.addMenu('&Display')
        display_menu.addAction(add_action)

        toolbar = self.addToolBar('toolbar')
        toolbar.addAction(exit_action)
        toolbar.addSeparator()
        toolbar.addAction(add_action)
        toolbar.addAction(edit_action)
        toolbar.addSeparator()
        toolbar.addAction(delete_action)


    def _init_content(self, widget):
        """loads table with displays"""
        displays = self.lcd_repository.find()
        if self.widgets['table_widget'] is not None:
            widget.removeWidget(self.widgets['table_widget'])
        table_widget = QTableWidget()
        table_widget.setColumnCount(0)
        table_widget.setColumnCount(4)
        table_widget.setRowCount(len(displays))
        table_widget.itemSelectionChanged.connect(self._select_row_action)
        table_widget.setHorizontalHeaderLabels(["Name", "Node name", "Size", "Stream"])
        row = 0
        for display in self.lcd_repository.find():
            item = QTableWidgetItem(display.name)
            item.setFlags(item.flags() & ~QtCore.Qt.ItemIsEditable)
            table_widget.setItem(row, 0, item)

            item = QTableWidgetItem(display.node_name)
            item.setFlags(item.flags() & ~QtCore.Qt.ItemIsEditable)
            table_widget.setItem(row, 1, item)

            item = QTableWidgetItem(str(display.get_size()[0]) + "x" + str(display.get_size()[1]))
            item.setFlags(item.flags() & ~QtCore.Qt.ItemIsEditable)
            table_widget.setItem(row, 2, item)

            item = QTableWidgetItem("Yes" if display.can_stream else "No")
            item.setFlags(item.flags() & ~QtCore.Qt.ItemIsEditable)
            table_widget.setItem(row, 3, item)

            row += 1

        table_widget.resizeRowsToContents()
        widget.addWidget(table_widget)
        self.widgets['delete_action'].setDisabled(True)
        self.widgets['edit_action'].setDisabled(True)
        self.widgets['table_widget'] = table_widget

    def _add_action(self):
        """starts form for add disply"""
        dialog = DisplayForm(
            self.lcd_repository.msg,
            self.lcd_repository.broadcast_ip,
            self.lcd_repository.broadcast_port
        )
        result = dialog.exec_()
        if result:
            display = dialog.get_display()
            self.lcd_repository.save_display(display)
            self._init_content(self.widgets['hbox'])

    def _delete_action(self):
        """delete action"""
        indexes = self.widgets['table_widget'].selectionModel().selectedRows()
        for index in sorted(indexes):
            item = self.widgets['table_widget'].item(index.row(), 0)
            self.lcd_repository.remove_by_name(item.text())
            self._init_content(self.widgets['hbox'])

    def _edit_action(self):
        """edit action - launch form"""
        indexes = self.widgets['table_widget'].selectionModel().selectedRows()
        index = indexes[0]
        item = self.widgets['table_widget'].item(index.row(), 0)
        displays = self.lcd_repository.find({'name': item.text()})
        dialog = DisplayForm(
            self.lcd_repository.msg,
            self.lcd_repository.broadcast_ip,
            self.lcd_repository.broadcast_port,
            displays[0]
        )
        result = dialog.exec_()
        if result:
            display = dialog.get_display()
            self.lcd_repository.save_display(display)
            self._init_content(self.widgets['hbox'])

    def _select_row_action(self):
        """called on table click, if row then enable delete and edit"""
        self.widgets['delete_action'].setDisabled(True)
        self.widgets['edit_action'].setDisabled(True)
        indexes = self.widgets['table_widget'].selectionModel().selectedRows()
        for index in sorted(indexes):
            self.widgets['delete_action'].setDisabled(False)
            self.widgets['edit_action'].setDisabled(False)

    def _closeEvent(self, event):
        """Called on close window"""
        reply = QMessageBox.question(self, 'Message', 'Are you sure?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()