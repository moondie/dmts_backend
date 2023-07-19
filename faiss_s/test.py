import requests as requests
from pymongo import MongoClient

import utils

client = MongoClient('mongodb://ewds:Hust5146279@127.0.0.1/ewds?authSource=admin')
s = utils.Requests()
headers = utils.Headers()
# 选择或创建数据库
db = client['ewds']

# 选择或创建集合
collection = db['repo_vector']
documents = collection.find()
for document in documents:
    if 'star' not in document.keys():
        collection.update_one({'_id': document['_id']}, {'$set': {'star': 0}})
    # url = document['url']
    # print(url)
    # username, repo = url.split('/')
    # api_url = f'https://api.github.com/repos/{username}/{repo}'
    # while True:
    #     try:
    #         response = s.get(api_url, headers=headers, timeout=(6.05, 7))
    #     except:
    #         print(f"网络错误")
    #         continue
    #     if response.status_code == 200:
    #         repo_info = response.json()
    #         star_count = repo_info['stargazers_count']
    #         # 更新文档，添加 star 属性
    #         collection.update_one({'_id': document['_id']}, {'$set': {'star': star_count}})
    #         print(f"已更新仓库 {url} 的 star 数量为: {star_count}")
    #         break
    #     elif response.status_code == 403:
    #         print(response.status_code)
    #         print(response.headers)
    #         print(response.text)
    #         print('Ratelimit, change token!')
    #         print(utils.token_p)
    #         headers = utils.NextHeaders()
    #     else:
    #         print(response.status_code)
    #         print(response.headers)
    #         print(response.text)
    #         print(f"获取仓库 {url} 信息失败")
    #         break