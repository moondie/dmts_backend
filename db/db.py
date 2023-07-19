import pymongo
from log import Log


class MongoDB():
    """
    连接 MongoDB 数据库，负责数据库数据层处理
    """

    def __init__(self, url="mongodb://root:LIwenke020@10.12.189.32:27017/") -> None:
        """根据 url 连接数据库和所需要的表"""
        self.__db = pymongo.MongoClient(url)["dmts"]
        self.__t_tasks = self.__db["tasks"]
        self.__t_repo_vector = self.__db["repo_vector"]
        self.__t_analysis_results = self.__db["analysis_results"]
        self.__logger = Log().logger

    def create_task(self, task_info) -> None:
        self.__t_tasks.insert_one(task_info)


    def get_task_list(self) -> list:
        """获取任务列表"""
        self.__logger.info("数据库读取任务列表")
        task_list = []
        for document in self.__t_tasks.find():
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

        self.__logger.info("数据库结束获取任务列表")
        return task_list

    def delete_task(self, task_id) -> bool:
        """删除任务"""
        self.__logger.info(f"数据库开始删除任务: {task_id}")
        if not self.__t_tasks.find_one({"taskId": task_id}):
            self.__logger.info(f"数据库删除任务不存在并结束: {task_id}")
            return False

        self.__t_tasks.update_one({"taskId": task_id}, {"$set": {"is_effective": False}})
        self.__logger.info(f"数据库删除任务并结束")
        return True

    def getVectors(self):
        data = self.__t_repo_vector.find()
        vecs = []
        sub_url_lst = []
        for document in data:
            vec = document['vector']
            sub_url = document['url']
            sub_url_lst.append(sub_url)
            vecs.append(vec)
        return vecs, sub_url_lst

    def getTask(self):
        return self.__t_tasks

    def getVector(self):
        return self.__t_repo_vector

    def getAnalysisResults(self):
        return self.__t_analysis_results

