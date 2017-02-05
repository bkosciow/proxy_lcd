#!/usr/bin/python3
# -*- coding: utf-8 -*-


class Display(object):
    def __init__(self, uuid, name, lcd, can_stream, node_type):
        self.name = name
        self.node_name = lcd.driver.node_names[0]
        self.lcd = lcd
        self.uuid = uuid
        self.can_stream = can_stream
        self.type = node_type

    def get_size(self):
        """gets lcd size"""
        return self.lcd.get_width(), self.lcd.get_height()

    def stream(self, content):
        """send data to lcd"""
        self.lcd.stream(content)
        self.lcd.flush()
