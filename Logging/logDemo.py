# coding: utf-8

import os
import time
import logging
from logging.handlers import RotatingFileHandler


class Logger:
    def __init__(self):
        """
        初始化
        """
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.INFO)

        today = time.strftime("%Y-%m-%d", time.localtime(time.time()))
        if not self.logger.handlers or self.logger.handlers[0].baseFilename.find(today) < 0:
            self.logger.handlers = []

            path = os.path.abspath(
                os.path.join(os.path.dirname((os.path.abspath(__file__))), "logfile"))
            if not os.path.exists(path):
                os.makedirs(path)

            log_filename = os.path.join(path, '{time}.log'.format(time=today))

            file_handler = RotatingFileHandler(log_filename, maxBytes=10240, encoding='utf-8')
            file_handler.setFormatter(
                logging.Formatter('%(asctime)s %(filename)s %(name)s line:%(lineno)d %(levelname)s %(message)s'))
            self.logger.addHandler(file_handler)
            file_handler.close()

    def getLogger(self):
        """
        获取初始化后的Logger
        :return:
        """
        return self.logger

if __name__ == '__main__':
    log = Logger().getLogger()
    log.info(u'信息级日志')
    log.warning(u'警告级日志')
    log.error(u'错误级日志')
    log.critical(u'严重级日志')
