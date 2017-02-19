#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author__ = 'Bartosz Kościów'

import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QCoreApplication
from service.tcp_server import StreamServer
from service.stream_content import StreamContent
from repository.config import Config
import getopt
import signal
signal.signal(signal.SIGINT, signal.SIG_DFL)

CLI = False


def parse_argv():
    global CLI
    try:
        params, args = getopt.getopt(sys.argv[1:], "c", ['cli'])
    except getopt.GetoptError as err:
        print(err)
        sys.exit(2)

    for o, v in params:
        if o == '--cli':
            CLI = True

if __name__ == '__main__':
    parse_argv()
    config = Config()

    if CLI:
        app = QCoreApplication(sys.argv)
    else:
        app = QApplication(sys.argv)

    stream_server = StreamServer(('0.0.0.0', config.server_port))
    stream_content = StreamContent(config)

    if not CLI:
        from views.main_view import MainView
        main_window = MainView(config)

    sys.exit(app.exec_())

