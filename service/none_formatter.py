#!/usr/bin/python3
# -*- coding: utf-8 -*-
from abstract.formatter import Formatter


class NoneFormatter(Formatter):

    def format(self, content, display):
        """return formatted content"""
        return content

    def get_name(self):
        """formatter name"""
        return "none"
