#!/usr/bin/env python
# -*- coding:utf-8 -*-

from gnet.interface import BaseClass

class UdpTunnel(BaseClass):

    def read(self, id):
        return self.lower_layer.read(id)

    def write(self, id, data):
        return self.lower_layer.write(id, data)

    def create_connection(self, address, kv=None):
        return self.lower_layer.create_connection(address, kv)

    def close_connection(self, id):
        return self.lower_layer.close_connection(id)
