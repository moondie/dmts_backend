import requests as requests
from requests.adapters import HTTPAdapter

tokens = ['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',
          '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',
          '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',
          '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',
          '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'
          ]
token_p = 0


def Headers():
    headers = {
        'Accept': 'application/vnd.github+json',
        'Authorization': 'Bearer ' + tokens[token_p],
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
    }
    return headers


def NextHeaders():
    global token_p
    token_p = (token_p + 1) % 5
    headers = {
        'Accept': 'application/vnd.github+json',
        'Authorization': 'Bearer ' + tokens[token_p],
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
    }
    return headers


def Requests():
    s = requests.session()
    s.mount('http://', HTTPAdapter(max_retries=5))
    s.mount('https://', HTTPAdapter(max_retries=5))
    return s
