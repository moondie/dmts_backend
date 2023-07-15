import pymongo
from log import Log


class MongoDB():
    """
    连接 MongoDB 数据库，负责数据库数据层处理
    """

    def __init__(self, url="mongodb://root:LIwenke020@localhost:27017/") -> None:
        """根据 url 连接数据库和所需要的表"""
        self._db = pymongo.MongoClient(url)["dmts"]
        self._t_tasks = self._db["tasks"]
        self._t_repo_vector = self._db["repo_vector"]
        self._t_analysis_results = self._db["analysis_results"]
        self._logger = Log().logger

    def get_task_list(self) -> list:
        """获取任务列表"""
        self._logger.info("开始获取任务列表")
        task_list = []
        for document in self._t_tasks.find():
            if not document["is_effective"]:
                continue

            task_list.append({
                "taskId": document["taskId"],
                "taskName": document["taskName"],
                "status": "running" if document["status"] in ("generated", "generating") else document["status"],
                "taskType": document["taskType"],
                "language": document["language"],
                "taskURL": document["taskURL"],
                "is_effective": document["is_effective"],
                "taskMode": document["taskMode"],
                "startTime": document["startTime"],
                "updateTime": document["updateTime"],
                "size": document["size"],
            })

        self._logger.info("结束获取任务列表")
        return task_list
