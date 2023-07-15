from flask import Flask, jsonify
from flask_cors import CORS

from log import Log
from task import TaskHandler

app = Flask(__name__)
CORS(app)

task_hander = TaskHandler()
logger = Log().logger


@app.route("/taskmanage/getTaskList", methods=["GET"])
def get_task_list():
    logger.info("网络请求-获取任务列表")
    return jsonify(task_hander.get_task_list())


if __name__ == "__main__":
    app.run(port=8001)
