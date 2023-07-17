from db import MongoDB
from log import Log


class TaskHandler():
    """处理任务请求"""

    def __init__(self) -> None:
        self.__db = MongoDB()
        self.__logger = Log().logger

    def get_task_list(self) -> list:
        """获得任务列表"""
        self.__logger.info("读取任务列表")
        return self.__db.get_task_list()

    def delete_task(self, task_id) -> bool:
        """删除任务"""
        self.__logger.info(f"删除任务: {task_id}")
        return self.__db.delete_task(task_id)
