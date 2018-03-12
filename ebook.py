#builtin module
from datetime import datetime

#pip install module
import requests
from bs4 import BeautifulSoup


import websocket
import json

import re

import random

URL_TPL = "https://www.packtpub.com/packt/offers/free-learning"
headers = {'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
def get_html(url) :
    _html = ""
    resp = requests.get(url, headers=headers)
    if resp.status_code == 200:
        _html = resp.text
    return _html

def parse_html(html):
    """입력받은 html에서 ebook의 책 제목 추출"""
    soup = BeautifulSoup(html, 'html.parser')
    ebook = soup.find("div",{"class":"dotd-title"})
    return ebook

#remove html tag
def rm_html_tags(data) :
    p = re.compile('<.*?>')
    p_text = re.sub(p, '', data)
    return p_text

def on_message(ws, message):
    message = json.loads(message)
    print(message)
    if 'type' in message.keys() and message['type'] != 'message':
        return
    html = get_html(URL_TPL)
    ebook = parse_html(html)
    str_ebook = str(ebook)
    ebook_name = rm_html_tags(str_ebook)
    if 'ebook' in message['text'] or 'eBook' in message['text'] or 'e북' in message['text'] or '이북' in message['text'] or 'Ebook' in message['text']:
        return_msg = {
            'channel': message['channel'],
            'type': 'message',
            'text': ebook_name.strip()
        }
        ws.send(json.dumps(return_msg))



# token = 'xoxb-313487174644-Yrri5dsn0uId0JApC651wVUP'
# get_url = requests.get('https://slack.com/api/rtm.connect?token=' + token)
# print(get_url.json()['url'])
# socket_endpoint = get_url.json()['url']
# print('Connecting to', socket_endpoint)
#
# websocket.enableTrace(True)
# ws = websocket.WebSocketApp(socket_endpoint, on_message=on_message)
# ws.run_forever()
