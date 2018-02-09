import subprocess
import signal
import logging
import threading
# from kutils.json_ipc import JsonClientSocket
from kutils.json_ipc import JsonServerMaster, JsonClientSocket
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

class Proxy(JsonServerMaster):
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
        super().__init__(json_ipc_socket)
        self.mitmprocess = self.start_mitmpdump()

    def start_mitmpdump(self):
        devnull = open('/dev/null', 'w')
        p = subprocess.Popen([MITMDUMP, '-q', '-s', self.mitmp_script, '-p', str(self.port)], stdout=devnull,
                                        shell=False)
        return p

    def stop(self):
        try:
            self.mitmprocess.send_signal(signal.SIGINT)
            super().stop() #TODO: fix kutils (JsonServerMaster.stop) a better way for server to shutdown and tell clients to quit
            # if self.up:
            #     self.up = False
            #     # os.kill(os.getpid(), signal.SIGINT)
            #     try:
            #         client = JsonClientSocket(self.server_address)
            #         client.connect()
            #         # client.quit() # TODO: remove this line
            #     except:
            #         pass
        except:
            pass

    def get_intercept_params(self):
        return {'domain': self.domain, 'paths': self.paths}

    def set_intercept_data(self, path, content):
        print('set_intercept_data:',id(self.intercept_data))
        self.intercept_data[path] = content

    def set_intercept_params(self, domain, paths):
        self.domain = domain
        self.paths = paths

    def get_intercept_data(self):
        res = dict(self.intercept_data)
        self.intercept_data.clear()
        return res