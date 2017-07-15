#!/usr/bin/python3


class Formatter(object):
    """Formatter class"""
    def __init__(self):
        self.formatters = {}

    def add(self, formatter):
        """add new formatter"""
        self.formatters[formatter.get_name()] = formatter

    def format(self, name, content):
        """calls proper formatter and returns content"""
        return self.formatters[name].format(content)

    def get_names(self):
        return self.formatters.keys()
