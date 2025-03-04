from ctypes import cdll, CFUNCTYPE, c_uint32, c_bool, c_void_p, c_char_p, c_ulong, POINTER, c_char
from .PlatformHelper import PlatformHelper as ph
from wtpy.WtUtilDefs import singleton
import os

CB_ON_MSG = CFUNCTYPE(c_void_p,  c_uint32, c_char_p, POINTER(c_char), c_uint32)
CB_ON_LOG = CFUNCTYPE(c_void_p,  c_uint32, c_char_p, c_bool)

# Python对接C接口的库
@singleton
class WtMQWrapper:
    '''
    Wt平台数据组件C接口底层对接模块
    '''

    # api可以作为公共变量
    api = None
    ver = "Unknown"
    
    # 构造函数，传入动态库名
    def __init__(self, logger = None):
        self._logger = logger
        dllname = ph.getModule("WtMsgQue")
        paths = os.path.split(__file__)
        a = (paths[:-1] + (dllname,))
        _path = os.path.join(*a)
        self.api = cdll.LoadLibrary(_path)

        self._cb_log = CB_ON_LOG(self.on_mq_log)
        self.api.regiter_callbacks(self._cb_log)

        self.api.create_server.argtypes = [c_char_p, c_bool]
        self.api.create_server.restype = c_ulong

    def on_mq_log(self, id:int, message:str, bServer:bool):
        message = bytes.decode(message)
        if self._logger is not None:
            self._logger.info(message)
        else:
            print(message)

    def create_server(self, url:str):
        return self.api.create_server(bytes(url, 'utf-8'), True)

    def destroy_server(self, id:int):
        self.api.destroy_server(id)

    def publish_message(self, id:int, topic:str, message:str):
        message = bytes(message, 'utf-8')
        self.api.publish_message(id, bytes(topic, 'utf-8'), message, len(message))

    def create_client(self, url:str, cbMsg:CB_ON_MSG):
        return self.api.create_client(bytes(url, 'utf-8'), cbMsg)

    def destroy_client(self, id:int):
        self.api.destroy_client(id)

    def subcribe_topic(self, id:int, topic:str):
        self.api.subscribe_topic(id, bytes(topic, 'utf-8'))

    def start_client(self, id:int):
        self.api.start_client(id)

