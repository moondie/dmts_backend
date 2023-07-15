import logging


class Log():
    """日志处理模块"""

    def __init__(self,
                 log_file="dmts.log",
                 log_level=logging.INFO,
                 log_format="%(asctime)s - %(levelname)s - %(filename)s:%(lineno)s - %(message)s") -> None:
        """根据日志等级和格式等生成日志示例"""
        self.__logger = logging.getLogger(__name__)
        self.__logger.setLevel(log_level)

        stdout_hander = logging.StreamHandler()
        stdout_hander.setFormatter(logging.Formatter(log_format))
        stdout_hander.setLevel(log_level)

        file_hander = logging.FileHandler(log_file)
        file_hander.setFormatter(logging.Formatter(log_format))
        file_hander.setLevel(log_level)

        # 防止多次注册处理器
        if not self.__logger.hasHandlers():
            self.__logger.addHandler(stdout_hander)
            self.__logger.addHandler(file_hander)

    @property
    def logger(self):
        return self.__logger
