import numpy as np
from flask import Flask, request, jsonify
import faiss_s

app = Flask(__name__)

fai = faiss_s.Faisss()


@app.route('/search', methods=['POST'])
def handle_request():
    data = request.get_json()

    vectors = data.get('vectors', [])
    vectors = [vectors]
    k = data.get('k', 50)
    ret,D = fai.search(np.array(vectors).astype('float32'), k)

    response = {
        'ids': ret,
        'D': D
    }
    return jsonify(response)


@app.route('/test', methods=['POST'])
def handle_test():

    response = {'ids': 'ret'}
    return jsonify(response)


if __name__ == '__main__':
    app.run()
