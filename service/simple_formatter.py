#!/usr/bin/python3
# -*- coding: utf-8 -*-
from abstract.formatter import Formatter


class SimpleFormatter(Formatter):

    def format(self, content, display):
        """return formatted content"""
        lines = content.splitlines()
        print(lines)
        # row = ""
        # print("---")
        # for letter in content:
        #     if letter not in ['\n', '\r\n']:
        #         row += letter
        #     else:
        #         print('nl')
        #         print(row)
        #         row = ""
        return content

    def get_name(self):
        """formatter name"""
        return "simple"
