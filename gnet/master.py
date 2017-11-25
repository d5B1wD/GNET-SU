#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys

class LoggerMaster(object):
    def __init__(self):
        self.loggers = []

    def add_logger(self, logger):
        self.loggers.append(logger)

    def debug(self, msg, *args, **kwargs):
        for i in self.loggers:
            i.debug(msg, *args, **kwargs)

    def info(self, msg, *args, **kwargs):
        for i in self.loggers:
            i.info(msg, *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        for i in self.loggers:
            i.warning(msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        for i in self.loggers:
            i.error(msg, *args, **kwargs)

    def critical(self, msg, *args, **kwargs):
        for i in self.loggers:
            i.critical(msg, *args, **kwargs)

class Master(object):

    def __init__(self):
        self.layers = []
        self.loggers = LoggerMaster()
        self.proxies = []

    def add_proxy(self, proxy):
        self.proxies.append(proxy)

    def start_proxy_server(self):
        pass

    def add_layer(self, new_layer):
        previous_layer = None

        if(len(self.layers)==0):
            previous_layer = self.proxies
        else:
            previous_layer = [self.layers[-1],]

        for i in previous_layer:
            i.set_lower_layer(new_layer)

        self.layers.append(new_layer)

    def add_logger(self, logger):
        self.loggers.add_logger(logger)

    def check_batch_process_results(self, results, caller_name=''):
        if not caller_name:
            caller_name = sys._getframe(2).f_code.co_name
        for i in results:
            if i[0]==False:
                self.loggers.warning("batch work '%s' result: %s %s",
                                        caller_name, i[1], str(i[0]))
            else:
                self.loggers.debug("batch work '%s' result: %s %s",
                                        caller_name, i[1], str(i[0]))

    def batch_work(self, func_name):
        res = []
        for i in self.layers:
            t = getattr(i, func_name)()
            res.append([t, str(type(i).__name__)])
        self.check_batch_process_results(res, func_name)

    def pre_start(self):
        self.batch_work(sys._getframe(0).f_code.co_name)

    def pre_stop(self):
        self.batch_work(sys._getframe(0).f_code.co_name)

    def stop(self):
        self.batch_work(sys._getframe(0).f_code.co_name)

    def post_stop(self):
        self.batch_work(sys._getframe(0).f_code.co_name)
