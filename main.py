from flask import Flask, jsonify
from flask_cors import CORS
import db

app = Flask(__name__)
CORS(app)

mongodb = db.MongoDB("mongodb://root:LIwenke020@localhost:27017/")

@app.route("/taskmanage/getTaskList")
def hello():
    return jsonify(mongodb.get_task_list())

@app.route("/taskmanage/getTaskList")
def hello():
    return jsonify(mongodb.get_task_list())

if __name__ == "__main__":
    app.run(port=8001)
