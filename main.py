from flask import Flask, jsonify, request
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


@app.route("/taskmanage/delete", methods=["POST"])
def delete_task():
    task_id = request.get_json()["taskId"]
    logger.info(f"网络请求-删除任务: {task_id}")
    rtn = task_hander.delete_task(task_id)
    return jsonify({"is_success": rtn})


if __name__ == "__main__":
    app.run(port=8001, debug=True)
