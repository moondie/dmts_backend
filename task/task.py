import datetime
import os
import re
import shutil
import threading
import time

import numpy as np
import requests
from bson import ObjectId

from db import MongoDB
from faiss_s import Faisss
from log import Log
from git import Repo


def get_level(number):
    if number == 0:
        return 0
    elif 1 <= number <= 4:
        return 1
    elif 5 <= number <= 10:
        return 2
    elif 11 <= number <= 20:
        return 3
    elif 21 <= number <= 50:
        return 4
    elif 51 <= number <= 100:
        return 5
    elif 101 <= number <= 200:
        return 6
    elif 201 <= number <= 400:
        return 7
    elif 401 <= number <= 700:
        return 8
    else:
        return 9


def get_product(arr1, arr2):
    dot_product = 0

    # calculate dot product
    for i in range(len(arr1)):
        dot_product += arr1[i] * arr2[i]

    return "{:.2f}".format(dot_product)


class TaskHandler:
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

    def create_task(self, task_info) -> dict:
        new_task = {
            **task_info,
            "taskId": f"Task_{str(ObjectId())}",
            "status": "running",
            "is_effective": True,
            "startTime": datetime.datetime.now().isoformat(),
            "updateTime": datetime.datetime.now().isoformat(),
        }
        self.__logger.info(f"创建任务: {new_task}")
        self.__db.create_task(new_task)
        threading.Thread(target=self.gitGet, args=(new_task['taskURL'],new_task['taskId'])).start()
        threading.Thread(target=self.AnalyseTask, args=(new_task['taskId'], new_task['taskMode'])).start()
        return True


    def gitGet(self, taskURL, taskId):
        regex = r'\/([^/]+)\/([^/]+)\.git$'
        match = re.search(regex, taskURL)
        if match:
            username = match.group(1)
            repo = match.group(2)
            sub_url = username + '/' + repo
            vector = self.__db.getVector()
            repo = vector.find_one({"url": sub_url})
            if repo:
                self.__logger.info(f"数据库中存在{sub_url}的向量")
            else:
                task_collection = self.__db.getTask()
                task = task_collection.find_one({"taskId": taskId})
                if task:
                    task['status'] = 'generating'
                    task_collection.update_one({"taskId": taskId}, {"$set": task})
                    self.__logger.info(f"数据库中更新{taskId}的状态为generating")
                else:
                    self.__logger.info(f"数据库中不存在{taskId}")
                dest = f'gitclone/{taskURL.replace(":", "_").replace("/", "_")}'
                if not os.path.exists(dest):
                    os.makedirs(dest)
                else:
                    # 删除文件夹内的文件
                    for filename in os.listdir(dest):
                        file_path = os.path.join(dest, filename)
                        try:
                            if os.path.isfile(file_path) or os.path.islink(file_path):
                                os.unlink(file_path)  # 删除文件或链接
                            elif os.path.isdir(file_path):
                                shutil.rmtree(file_path)  # 删除目录
                        except Exception as e:
                            self.__logger.info(f"删除文件夹内的文件失败{e}")

                try:
                    Repo.clone_from(taskURL, dest)
                    self.__logger.info(f"git clone成功")
                    data = {
                        'path': f'C:/Users/hongs/dmts_backend/{dest}',
                        'url': sub_url,
                        'task_id': taskId
                    }

                    try:
                        resp = requests.post('http://localhost:5001/generateVector', data=data)
                        if resp.status_code == 200:
                            self.__logger.info(f"向量生成成功")
                        else:
                            self.__logger.info(f"向量生成失败")
                    except Exception as e:
                        self.__logger.info(f"向量生成失败{e}")
                except Exception as e:
                    self.__logger.info(f"git clone失败{e}")

        else:
            self.__logger.info(f"taskURL格式错误")
        self.__logger.info(f"gitGet成功")

    def AnalyseTask(self, taskId):
        tasks = self.__db.getTask()
        while True:
            task = tasks.find_one({"taskId": taskId})
            if task:
                if task['status'] == 'generating':
                    self.__logger.info(f"等待生成向量5s")
                    time.sleep(5)
                else:
                    break

            else:
                self.__logger.info(f"数据库中不存在{taskId}")
                return

        task = tasks.find_one({"taskId": taskId})
        regex = r'\/([^/]+)\/([^/]+)\.git$'
        match = re.search(regex, task['taskURL'])
        if match:
            username = match.group(1)
            repo = match.group(2)
            sub_url = username + '/' + repo
            repo_vectors = self.__db.getVector()
            repo_v = repo_vectors.find_one({"url": sub_url})
            if repo_v:
                vectors = [repo_v['vectors']]
                k = 50
                language = ''
                size = 0
                try:
                    resp = requests.get('https://api.github.com/repos/' + sub_url)
                    if resp.status_code == 200:
                        language = resp.json()['language']
                        if language == 'C++' or language == 'C':
                            language = 'C/C++'

                        size = resp.json()['size']
                        faiss = Faisss()
                        results, Ds = faiss.search(np.array(vectors).astype('float32'), k)
                        result = results[0]
                        D = Ds[0]
                        for i in range(len(result)):
                            result[i] = 'https://github.com/' + result[i]
                        for i in range(len(D)):
                            D[i] = round(D[i] * 100, 2)
                            if D[i] > 100:
                                D[i] = 100.00
                        associated_repo_objs = []
                        for i in range(len(result)):
                            associated_repo_obj = {'url': result[i], 'similarity': D[i]}
                            threat_level = 0
                            product_layout = 0
                            product_lexical = 0
                            product_syntactic = 0
                            repo1 = repo_vectors.find_one({"url": results[0][i][19:]})
                            if repo1:
                                stars = 0
                                resp2 = requests.get('https://api.github.com/repos/' + repo1['url'])
                                if resp2.status_code == 200:
                                    stars = resp2.json()['stargazers_count']
                                threat_level = get_level(stars)
                                product_layout = get_product(repo_v['layout_vec'], repo1['layout_vec'])
                                product_lexical = get_product(repo_v['lexical_vec'], repo1['lexical_vec'])
                                product_syntactic = get_product(repo_v['syntactic_vec'], repo1['syntactic_vec'])
                            associated_repo_obj['threat_level'] = threat_level
                            associated_repo_obj['product_layout'] = product_layout
                            associated_repo_obj['product_lexical'] = product_lexical
                            associated_repo_obj['product_syntactic'] = product_syntactic
                            associated_repo_objs.append(associated_repo_obj)
                        analysis_result = {
                            'taskId': taskId,
                            'vectors': repo_v.vector,
                            'associated_repo_objs': associated_repo_objs,
                            'userName': username,
                            'status': "Stopped",
                        }
                        self.__db.getAnalysisResults().insert_one(analysis_result)
                        tasks.update_one({"taskId": taskId}, {"$set": {"status": "success",
                                                                       'updateTime': datetime.datetime.now().isoformat(),
                                                                       'language': language,
                                                                        'size': size,
                                                                       }})
                    else:
                        self.__logger.info(f"获取仓库信息失败,网络错误")
                except Exception as e:
                    self.__logger.info(f"获取仓库信息失败，{e}")
            else:
                self.__logger.info(f"数据库中不存在{sub_url}的向量")
