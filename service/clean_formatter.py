#!/usr/bin/python3
# -*- coding: utf-8 -*-
from abstract.formatter import Formatter
import re


class CleanFormatter(Formatter):
    def format(self, content, display):
        """return formatted content"""
        pattern = re.compile(r'\s+')
        return pattern.sub(' ', content)

    def get_name(self):
        """formatter name"""
        return "clean"
