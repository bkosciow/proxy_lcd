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


def print_config(config):
    print("Config loaded. Starting app")
    print("TCP port: ", config.server_port)
    print("Broadcast IP: ", config.broadcast_ip)
    print("Broadcast port: ", config.broadcast_port)
    print("LCDs:")
    print("{:<10} | {:<10} | {:<7} | {:<6} | {:<8}".format('Name', 'Node name', 'Size', 'Stream', 'Type'))
    for lcd in config.find_all():
        size = lcd.get_size()
        print("{:<10} | {:<10} | {:<7} | {:<6} | {:<8}".format(
            lcd.name,
            lcd.node_name,
            str(size[0]) + "," + str(size[1]),
            '+' if lcd.can_stream else '-',
            lcd.type
        ))


if __name__ == '__main__':
    parse_argv()
    config = Config()

    if CLI:
        print_config(config)
        app = QCoreApplication(sys.argv)
    else:
        app = QApplication(sys.argv)

    stream_server = StreamServer(('0.0.0.0', config.server_port))
    stream_content = StreamContent(config)

    if not CLI:
        from views.main_view import MainView
        main_window = MainView(config)

    sys.exit(app.exec_())
