# -*-coding:utf-8 -*-
import logging
import os.path
import time

from MonkeyTest.Common.utils import get_phone_time


class Logger:

    def __init__(self, logger, FilePath, device, CmdLevel=logging.INFO, FileLevel=logging.INFO, log_type='app'):
        self.logger = logging.getLogger(logger)
        # 设置日志输出的默认级别
        self.logger.setLevel(logging.DEBUG)
        time_value = str(get_phone_time(device=device) + '- %(filename)s:[%(lineno)s] - [%(levelname)s] - %(message)s')
        # 日志输出格式
        # fmt = logging.Formatter('%(asctime)s - %(filename)s:[%(lineno)s] - [%(levelname)s] - %(message)s')
        fmt = logging.Formatter(time_value)
        currentTime = time.strftime("%Y-%m-%d")
        if log_type == "system":
            self.logFileName = FilePath + '\\' + currentTime + ".log"
        else:
            # 获取路径下所有文件夹的数量
            # 创建新的文件夹
            # 更新log文件存放路径
            currentTime = time.strftime("%Y-%m-%d-%H-%M-%S")
            self.logFileName = FilePath + '\\' + currentTime + ".log"
        # 文件输出到磁盘中
        fh = logging.FileHandler(self.logFileName)
        fh.setFormatter(fmt)
        fh.setLevel(FileLevel)

        self.logger.addHandler(fh)

    def debug(self, msg):
        self.logger.debug(msg)

    def info(self, msg):
        self.logger.info(msg)

    def warn(self, msg):
        self.logger.warning(msg)

    def error(self, msg):
        self.logger.error(msg)

    def critical(self, msg):
        self.logger.critical(msg)


if __name__ == '__main__':
    logger = Logger("fox",FilePath="D:\\log\\",device="HA1WQRBK", CmdLevel=logging.DEBUG, FileLevel=logging.DEBUG)
    logger.logger.debug("debug")
    logger.logger.log(logging.ERROR, '%(module)s %(info)s', {'module': 'log日志', 'info': 'error'})
