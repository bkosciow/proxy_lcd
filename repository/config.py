#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author__ = 'Bartosz Kościów'
from configparser import ConfigParser
from iot_message import message
from charlcd.drivers.wifi_content import WiFi
from charlcd.buffered import CharLCD
from model.display import Display


class Config(object):
    filters = {'name', 'can_stream', 'node_name'}

    def __init__(self, file="config/settings.ini"):
        self.config = ConfigParser()
        self.config.read(file)
        self.node_name = self.config.get("general", "node_name")
        self.msg = message.Message(self.node_name)
        self.broadcast_ip = self.config.get("general", "broadcast_ip")
        self.server_port = int(self.config.get("general", "server_port"))
        if not self.broadcast_ip:
            self.broadcast_ip = '<broadcast>'
        self.broadcast_port = int(self.config.get("general", "broadcast_port"))
        self.displays = []
        self.file = file
        self.load_lcd()

    def load_lcd(self):
        """finds lcd's section"""
        self.displays = []
        for section in self.config.sections():
            if section[0:3] == "lcd":
                self.create_display(section)

    def create_display(self, section):
        """create Display from cfg section"""
        drv = WiFi(self.msg, [self.config.get(section, "node_name")], (self.broadcast_ip, self.broadcast_port))
        width, height = (self.config.get(section, "size")).split("x")
        lcd = CharLCD(int(width), int(height), drv)
        lcd.init()
        self.displays.append(
            Display(
                section,
                self.config.get(section, "name"),
                lcd,
                self.config.getboolean(section, "stream"),
                self.config.get(section, "type")
            )
        )

    def save_display(self, display):
        if display.uuid is None:
            section = 'lcd' + '-' + display.name
            self.config.add_section(section)
        else:
            section = display.uuid

        size = display.get_size()
        self.config.set(section, 'name', display.name)
        self.config.set(section, 'size', str(size[0]) + 'x' + str(size[1]))
        self.config.set(section, 'node_name', display.node_name)
        self.config.set(section, 'stream', '1' if display.can_stream else '0')
        self.config.set(section, 'type', display.type)
        self.load_lcd()
        self.save_config()

    def remove_by_name(self, name):
        """remove section by name"""
        section = self._find_section_by_name(name)
        self.config.remove_section(section)
        self.load_lcd()
        self.save_config()

    def _find_section_by_name(self, name):
        for section in self.config.sections():
            if section is not None and section[0:3] == "lcd" and self.config.get(section, 'name') == name:
                return section
        return None

    def save_config(self):
        """save config to file"""
        with open(self.file, "w") as f:
            self.config.write(f)

    def find_all(self):
        """return all displays"""
        return self.displays

    def find(self, filters=[]):
        """filter displays by criteia"""
        for f in filters:
            if f not in self.filters:
                raise Exception('incorrect filter ' + str(f))

        results = self.find_all()

        if 'name' in filters:
            results = (i for i in results if i.name == filters['name'])

        if 'node_name' in filters:
            results = (i for i in results if i.node_name == filters['node_name'])

        if 'can_stream' in filters:
            results = (i for i in results if i.can_stream == filters['can_stream'])

        return list(results)
