import pymongo

class MongoDB():
    def __init__(self, url) -> None:
        self._db = pymongo.MongoClient(url)["dmts"]
        self._t_tasks = self._db["tasks"]
        self._t_repo_vector = self._db["repo_vector"]
        self._t_analysis_results = self._db["analysis_results"]

    def get_task_list(self) -> list:
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

        return task_list
