#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author__ = 'Bartosz Kościów'

import sys
from PyQt5.QtWidgets import QApplication
from views.main_view import MainView
from service.tcp_server import StreamServer
from service.stream_content import StreamContent
from repository.config import Config


if __name__ == '__main__':
    app = QApplication(sys.argv)
    config = Config()

    stream_server = StreamServer(('localhost', config.server_port))
    stream_content = StreamContent(config)
    main_window = MainView(config)

    sys.exit(app.exec_())
