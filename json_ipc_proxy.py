from kutils.json_ipc import JsonServerProxy
from kutils.logs import configure_logging
import logging
import time
logger= logging.getLogger(__name__)


def shell(flow):
    while True:
        cmd = input('\n>>> ')
        if cmd == 'break':
            break
        print(eval(cmd))

class Intercept:
    def __init__(self):
        self.domain = ''
        self.paths = []
        self.intercepted_data = {}
        self.proxy = JsonServerProxy("proxy-socket")
        self.last_intercept_update = 0.0
        self.update_intercept_data()

    def update_intercept_data(self):
        t1 = time.time()
        if t1 - self.last_intercept_update > 1.0:
            ret = self.proxy.get_intercept_params()
            self.domain, self.paths = ret['domain'], ret['paths']
            self.last_intercept_update = t1

    def response(self, flow):
        # self.update_intercept_data()
        logger.debug("intercepted url: %s", self.domain+flow.request.path)
        if flow.request.host == self.domain and flow.request.path in self.paths:
            flow.intercept()
            # flow.request.query['whatever parameter you want to change'] = v$
            flow.resume()
            # logger.info('Intercepted path: %s', flow.request.path)
            # logger.debug(str(type(flow.response.content)))
            self.proxy.set_intercept_data(path=flow.request.path, content=flow.response.text)
            logger.info('sent data for path: %s', flow.request.path)
            # self.update_intercept_data()
            # shell(flow)
            # self.client.call_function('set_intercept_data', {'path': flow.request.path, 'content': 'test'})
            # print(flow.response.content)


    def set_intercept_params(self, domain, paths):
        self.domain = domain
        self.paths = paths

    def get_intercepted_data(self):
        res =  dict(self.intercepted_data)
        self.intercepted_data.clear()
        return res


def start():
    global proxy
    configure_logging(modules=[__name__], level='INFO')
    proxy = Intercept()
    return proxy


def done():
    try:
        proxy.client.quit()
        proxy.client.close()
    except:
        pass


# def start():
#     global proxy
#     configure_logging(modules=['kutils', 'xaled-selenium'])
#     proxy = Intercept()
#     t = Thread(target=server_main())
#     t.start()
#     print('returning proxy')
#     return proxy
#
#
# def server_main():
#     server = JsonServerSocket('proxy-socket', server_callback)
#     server.bind()
#     while True:
#         try:
#             connection, client_address = server.accept()
#             while connection.receive_call():
#                 pass
#         except KeyboardInterrupt:
#             try:
#                 server.close()
#             finally:
#                 raise
#         except Exception as e:
#             logger.error("Error in control server: %s", e, exc_info=True)
#             if connection is not None:
#                 try:
#                     connection.close()
#                 finally:
#                     server.reconnect()
#
# def server_callback(function, arguments):
#     global proxy
#     if function == 'set_intercept_params':
#         return proxy.set_intercept_params(**arguments)
#     elif function == 'get_intercepted_data':
#         return proxy.get_intercepted_data()
#     else:
#         return None

