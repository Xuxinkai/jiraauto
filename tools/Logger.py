import logging
import os
import time


class logs(object):

    def __init__(self, name=None):
        self.name = name
        # ①创建一个记录器
        self.logger = logging.getLogger(self.name)
        self.logger.setLevel("INFO")  # 设置日志级别为 'level'，即只有日志级别大于等于'level'的日志才会输出
        self.formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")  # 创建formatter
        # ②创建屏幕-输出到控制台，设置输出等级
        self.streamHandler = logging.StreamHandler()
        self.streamHandler.setLevel("DEBUG")
        # ③创建log文件，设置输出等级
        PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # 根目录
        time_now = time.strftime('%Y_%m%d_%H', time.localtime()) + '.log'  # log文件命名：2022_0402_21.log
        self.fileHandler = logging.FileHandler(os.path.join(PROJECT_ROOT, "log", time_now), 'a', encoding='utf-8')
        self.fileHandler.setLevel("DEBUG")
        # ④用formatter渲染这两个Handler
        self.streamHandler.setFormatter(self.formatter)
        self.fileHandler.setFormatter(self.formatter)
        # ⑤将这两个Handler加入logger内
        self.logger.addHandler(self.streamHandler)
        self.logger.addHandler(self.fileHandler)

    def getLogger(self):
        return self.logger
