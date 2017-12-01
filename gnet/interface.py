#!/usr/bin/env python
# -*- coding:utf-8 -*-

'''interface for all sub class.

for now, there's only `set_master` method.

'''

import sys

DATA = {}

class NotImplementException(Exception):
    def __init__(self):
        super(NotImplementException, self).__init__()
        caller_frame = sys._getframe(1)
        f_name = caller_frame.f_code.co_name
        class_name = caller_frame.f_locals['self'].__class__.__name__
        self.args = [__file__, f_name, class_name]
        self.message = 'function not implement yet!'


class BaseClass(object):

    def __init__(self):
        self.master = None
        self.lower_layer = None
        self.upper_layer = None
        self.logger = None

    def create_connection(self, address, kv=None):
        raise NotImplementException()

    def close_connection(self, id):
        raise NotImplementException()

    def read(self, sid):
        raise NotImplementException()

    def write(self, sid, data):
        raise NotImplementException()

    def set_master(self, master):
        self.master = master

    def set_lower_layer(self, lower_layer):
        self.lower_layer = lower_layer

    def set_logger(self, logger):
        self.logger = logger

    def pre_start(self):
        return True

    def post_start(self):
        return True

    def start(self):
        return True

    def pre_stop(self):
        return True

    def post_stop(self):
        return True

    def stop(self):
        return True

