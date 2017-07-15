#!/usr/bin/python3
# -*- coding: utf-8 -*-
from abstract.formatter import Formatter
import math
import re


class SimpleFormatter(Formatter):

    def format(self, content, display):
        """return formatted content"""
        lines = []
        pattern = re.compile(r'\s+')
        for line in content.splitlines():
            line = pattern.sub(' ', line)
            if len(line) < display.lcd.get_width():
                lines.append(line.ljust(display.lcd.get_width()))
            else:
                chunks = math.ceil(len(line)/display.lcd.get_width())
                for chunk in range(chunks):
                    subline = line[
                        chunk*display.lcd.get_width():
                        chunk*display.lcd.get_width()+display.lcd.get_width()
                    ]
                    lines.append(subline.ljust(display.lcd.get_width()))

        return "".join(lines)

    def get_name(self):
        """formatter name"""
        return "simple"
