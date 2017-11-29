import eventlet

BASE_PROXY_STATUS_NORMAL = 0
BASE_PROXY_STATUS_GOING_STOP = 1
BASE_PROXY_STATUS_STOPPED = 2


class BaseProxy(object):
    def __init__(self, host='127.0.0.1', port=18901):
        self.host = host
        self.port = port
        self.sessions = {}
        self.lower_layer = None
        self.logger = None
        self.status = BASE_PROXY_STATUS_NORMAL
        self.server = None

    def _do_exchange(self, client, target_sid, direction):
        if direction == 0:
            while True:
                try:
                    data = client.recv(40960)
                except Exception as e:
                    self.logger.error("sid:%s read from client Exception:%s %s" % (target_sid, e.message, str(e.args)))
                    data = None
                if not data:
                    break
                target_sid.send(data)
        else:
            while True:
                data = target_sid.read(40960)
                if not data:
                    break
                try:
                    client.sendall(data)
                except Exception as e:
                    self.logger.error("sid:%s write to client Exception:%s %s" % (target_sid, e.message, str(e.args)))
                    break
        if target_sid in self.sessions:
            elem = self.sessions.pop(target_sid)
            self.close_connection(*elem)

    def do_exchange(self, client, target_sid):
        self.sessions[target_sid] = [client, target_sid]
        eventlet.spawn_n(self._do_exchange, self,  client, target_sid, 0)
        self._do_exchange(client, target_sid, 1)

    def get_target_address(self, client_connection):
        raise Exception()

    def pre_exchange(self, target_info, sid):
        raise Exception()

    def new_connection(self, client_connection, address):
        target_info = self.get_target_address(client_connection)
        target_address = target_info['address']
        self.logger.debug("accept new connection %s ===> %s" % (str(address), str(target_address)))
        sid = self.lower_layer.make_new_connection(target_address)
        if sid:
            need_exchange = self.pre_exchange(target_info, sid)
            if need_exchange:
                self.do_exchange(client_connection, sid)
            else:
                self.close_connection(client_connection, sid)
        else:
            try:
                client_connection.close()
            except Exception as e:
                pass

    def close_connection(self, client_connection, sid):
        if client_connection:
            try:
                client_connection.close()
            except Exception as e:
                pass
        if sid:
            sid.close()

    def start_server(self):
        self.server = eventlet.listen((self.host, self.port))
        while self.status == BASE_PROXY_STATUS_NORMAL:
            new_connection, address = self.server.accept()
            self.new_connection(new_connection, address)
        self.status = BASE_PROXY_STATUS_STOPPED

    def stop_server(self):
        self.status = BASE_PROXY_STATUS_GOING_STOP
        while True:
            eventlet.sleep(1)
            if self.status == BASE_PROXY_STATUS_STOPPED:
                break
