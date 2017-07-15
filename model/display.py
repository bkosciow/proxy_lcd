#!/usr/bin/python3
# -*- coding: utf-8 -*-
import service.errors_print


class Display(object):
    def __init__(self, uuid, name, lcd, can_stream, node_type, formatter):
        self.name = name
        self.node_name = lcd.driver.node_names[0]
        self.lcd = lcd
        self.uuid = uuid
        self.can_stream = can_stream
        self.type = node_type
        self.formatter = formatter

    def get_size(self):
        """gets lcd size"""
        return self.lcd.get_width(), self.lcd.get_height()

    def stream(self, content, formatter=None):
        """send data to lcd"""
        if formatter is not None:
            content = formatter.format(content, self)
        self.lcd.stream(content)
        self.lcd.flush()
