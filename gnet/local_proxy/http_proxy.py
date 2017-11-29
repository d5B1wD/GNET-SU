from gnet.local_proxy.base_proxy import BaseProxy
from gnet.interface import BaseClass


class HttpProxy(BaseProxy, BaseClass):

    def get_target_address(self, client_connection):
        pass

    def pre_exchange(self, target_info, sid):
        client_connection = target_info['client_connection']
        print client_connection
        return False
