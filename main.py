from flask import Flask, jsonify
from flask_cors import CORS

from log import Log
from db import MongoDB

app = Flask(__name__)
CORS(app)

mongodb = MongoDB()
logger = Log().logger


@app.route("/taskmanage/getTaskList")
def get_task_list():
    logger.info("获取任务列表")
    return jsonify(mongodb.get_task_list())


if __name__ == "__main__":
    app.run(port=8001)
