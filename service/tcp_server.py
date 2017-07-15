#!/usr/bin/python3
# -*- coding: utf-8 -*-

from PyQt5.QtNetwork import QTcpServer, QHostAddress, QTcpSocket, \
    QAbstractSocket
from PyQt5.QtCore import QThread
from service.signals import SIGNALS


class StreamServer(QTcpServer):
    def __init__(self, address):
        super().__init__()
        self.listen(QHostAddress(address[0]), address[1])

    def incomingConnection(self, socket):
        """handle new connection"""
        thread = StreamContent(self, socket)
        thread.start()


class StreamContent(QThread):
    def __init__(self, parent, socket):
        super().__init__(parent)
        self.socket = socket
        self.parent = parent

    def run(self):
        """handle communication"""
        tcp_socket = QTcpSocket()
        tcp_socket.setSocketDescriptor(self.socket)
        while tcp_socket.state() == QAbstractSocket.ConnectedState:
            try:
                tcp_socket.waitForReadyRead()
                data = tcp_socket.readAll()
                data = bytes(data).decode()
                SIGNALS['stream'].state.emit(data)
            except Exception as e:
                print(e)
                raise
