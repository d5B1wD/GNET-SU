from gnet.local_proxy.base_proxy import BaseProxy
from gnet.interface import BaseClass
from eventlet.green import socket
import struct


class Sock5Helper(object):

    def __init__(self, client_sock):
        self.client_sock = client_sock

    def get_all_peer_info(self):
        client = self.client_sock
        # version
        data = client.recv(262)
        if data[0] != '\x05':
            try:
                client.close()
            except:
                pass
            return
        client.send('\x05\x00')

        # Request
        r_file = client.makeifle('r')
        data = r_file.read(4)
        method = ord(data[1])
        reply = ''
        if method != 1 and method != 3:
            reply = '\x05\x07\x00\x01\x00\x00\x00\x00\x00\x00'
        else:
            ip_type = ord(data[3])
            ip_addr = ''
            if ip_type == 1:
                ip_addr = socket.inet_ntoa(r_file.read(4))
            elif ip_type==3:
                len = ord(r_file.read(1)[0])
                ip_addr = r_file.read(len)
            else:
                reply = '\x05\x08\x00\x01\x00\x00\x00\x00\x00\x00'
            ip_port = struct.unpack('!H', r_file.read(2))

        if reply:
            # error happens
            try:
                client.sendall(reply)
                client.close()
            except:
                pass
            return

        return False


class Sock5Proxy(BaseProxy, BaseClass):

    def get_target_address(self, client_connection):
        target_info = {}
        target_info['sock5_helper'] = Sock5Helper(client_connection)
        try:
            pass
        except Exception as e:
            host, port = socket.getnameinfo(client_connection)
            self.logger.info("Exception for %s:%s, %s, %s" %
                             (str(host), str(port),e.message, str(e.args)))
            return {}

    def pre_exchange(self, target_info, sid):
        client_connection = target_info['client_connection']
        print client_connection
        return False
