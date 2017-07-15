#!/usr/bin/python3
# -*- coding: utf-8 -*-
import abc


class Formatter(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def format(self, content, display):
        """return formatted content"""
        pass

    @abc.abstractmethod
    def get_name(self):
        """formatter name"""
        pass
