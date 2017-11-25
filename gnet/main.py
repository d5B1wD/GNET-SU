#!/usr/bin/env python
# -*- coding:utf-8 -*-

from gnet.local_proxy import Sock5Proxy, HttpProxy
from gnet.crypto import Crypto
from gnet.mixer import SimpleMixer
from gnet.udp_tunnel import UdpTunnel

from gnet.master import Master

if __name__=='__main__':
    master = Master()

    master.add_proxy(Sock5Proxy())
    master.add_proxy(HttpProxy())

    master.add_layer(Crypto())

    master.add_layer(SimpleMixer())

    master.add_layer(UdpTunnel())

    master.pre_start()

    master.start_proxy_server()

    master.pre_stop()

    master.stop()

    master.post_stop()
