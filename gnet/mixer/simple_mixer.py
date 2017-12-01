#!/usr/bin/env python
# -*- coding:utf-8 -*-

from gnet.interface import BaseClass


class SimpleMixer(BaseClass):

    def read(self, sid):
        return self.lower_layer.read(sid)

    def write(self, id, data):
        return self.lower_layer.write(id, data)

    def create_connection(self, address, kv=None):
        return self.lower_layer.create_connection(address, kv)

    def close_connection(self, id):
        return self.lower_layer.close_connection(id)
