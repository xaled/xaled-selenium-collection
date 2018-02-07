import subprocess
import signal
import logging
import threading
# from kutils.json_ipc import JsonClientSocket
from kutils.json_ipc import JsonServerSocket
from xaled_selenium.config import MITMDUMP, MITMP_SCRIPT
logger = logging.getLogger(__name__)



# class Proxy:
#     def __init__(self, port=8080, json_ipc_socket="proxy-socket", mitmp_script=MITMP_SCRIPT):
#         self.port = port
#         self.json_ipc_socket = json_ipc_socket
#         self.mitmp_script = mitmp_script
#         self.process = None
#         self.proxy_address = '127.0.0.1:%d' % port
#         # self.start()
#         self.client = JsonClientSocket(self.json_ipc_socket)
#         self.client.connect()
#
#     def start(self):
#         devnull = open('/dev/null', 'w')
#         self.process = subprocess.Popen([MITMDUMP, '-q', '-s', self.mitmp_script, '-p', self.port], stdout=devnull,
#                                         shell=False)
#         return self.process
#
#     def close(self):
#         try:
#             self.process.send_signal(signal.SIGINT)
#             self.client.close()
#         except:
#             pass
#
#     def set_intercept_params(self, domain, paths):
#         return self.client.call_function('set_intercept_params', {'domain': domain, 'paths': paths})
#
#     def get_intercept_data(self):
#         return self.client.call_function('get_intercept_data')


class Proxy:
    def __init__(self, port=8080, json_ipc_socket="proxy-socket", mitmp_script=MITMP_SCRIPT, domain='', paths=list()):
        self.port = port
        self.json_ipc_socket = json_ipc_socket
        self.mitmp_script = mitmp_script
        self.process = None
        self.server = None
        self.proxy_address = '127.0.0.1:%d' % port
        # self.start()
        # self.server = JsonServerSocket(self.json_ipc_socket, )
        self.up = True
        self.domain = domain
        self.paths = paths
        self.intercept_data = {}

    def server_main(self):
        self.server = JsonServerSocket(self.json_ipc_socket, self.server_callback)
        self.server.bind()
        while self.up:
            try:
                connection, client_address = self.server.accept()
                while connection.receive_call():
                    pass
            except KeyboardInterrupt:
                try:
                    self.server.close()
                finally:
                    raise
            except Exception as e:
                logger.error("Error in control server: %s", e, exc_info=True)
                if connection is not None:
                    try:
                        connection.close()
                    finally:
                        self.server.reconnect()

    def server_callback(self, function, arguments):
        if function == 'get_intercept_params':
            return {'domain': self.domain, 'paths': self.paths}
        elif function == 'set_intercept_data':
            self.intercept_data[arguments['path']] = arguments['content']
        else:
            return

    def start(self):
        t = threading.Thread(target=self.server_main)
        t.setDaemon(True)
        t.start()
        # devnull = open('/dev/null', 'w')
        # self.process = subprocess.Popen([MITMDUMP, '-q', '-s', self.mitmp_script, '-p', self.port], stdout=devnull,
        #                                 shell=False)
        # return self.process

    def close(self):
        self.up =  False
        try:
            self.process.send_signal(signal.SIGINT)
            self.server.close()
        except:
            pass

    def set_intercept_params(self, domain, paths):
        self.domain = domain
        self.paths = paths

    def get_intercept_data(self):
        res = dict(self.intercept_data)
        self.intercept_data.clear()
        return res