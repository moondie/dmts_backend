import json
import os

import utils

userlist = os.listdir('UsersInfo')


s = utils.Requests()
headers = utils.Headers()
for filename in userlist:
    id = filename[0:-5]

    fp = open(f'reposInfo/{id}.json','w')
    print(id)
    url = url = 'https://api.github.com/search/repositories?q=user:' + id + '+language:c+language:java+language:c%2B%2B&per_page=100'
    while True:
        try:
            print('get ' + id)
            resp = s.get(url=url, headers=headers, timeout=(6.05, 7))
        except:
            print(id + ' err')
            continue
        if resp.status_code == 200:
            dict_resp = resp.json()
            json.dump(dict_resp,fp=fp,indent=1)
            break
        elif resp.status_code == 403:
            print(resp.status_code)
            print(resp.headers)
            print(resp.text)
            print('Ratelimit, change token!')
            headers = utils.NextHeaders()
        else:
            print(resp.status_code)
            print(resp.headers)
            print(resp.text)
            print(id + ' err!')
            break