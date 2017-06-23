#!/usr/bin/python3
# -*- coding: utf-8 -*-

from service.signals import SIGNALS
import json


class StreamContent(object):
    def __init__(self, lcd_repository):
        self.lcd_repository = lcd_repository
        SIGNALS['stream'].state.connect(self.handle_stream)

    def handle_stream(self, content):
        """send content to display"""
        content = content.strip()
        message = self._decode(content)
        if message and 'protocol' in message and message['protocol'] == 'proxylcd':
            self._handle_command(message)
        else:
            self._send_stream(content)

    def _decode(self, content):
        """decode content to message"""
        try:
            message = json.loads(content)
            if type(message) != dict:
                message = None
        except ValueError:
            message = None

        return message

    def _send_stream(self, content):
        """stream content to nodes with stream enabled"""
        displays = self.lcd_repository.find({'can_stream': True})
        for display in displays:
            display.stream(content)

    def _send_message_to_node(self, message):
        """send message to target node"""
        displays = self.lcd_repository.find({'node_name': message['target']})
        for display in displays:
            display.stream(message['content'])

    def _handle_command(self, command):
        """handle a message"""
        if 'command' not in command:
            return

        if command['command'] == 'clear':
            displays = self.lcd_repository.find({'can_stream': True})
            for display in displays:
                display.lcd.buffer_clear()
                display.lcd.set_xy(0, 0)


