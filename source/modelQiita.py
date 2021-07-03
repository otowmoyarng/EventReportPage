from commonlogger import getLogger, IsDebug
from datetime import date
from typing import Dict
import json
import requests

BASE_URL = "https://qiita.com/api/v2/items"
TOKEN = ""
RANKING_EN = ["one","two","three","four","five"]

def PostQiita(startdate: date, enddate: date, allevents: Dict, isDebug: bool = False) -> None:
    """[summary]
        イベントデータをQiitaに投稿する
    Args:
        startdate (date): 抽出日From
        enddate (date): 抽出日To
        allevents (Dict): イベントデータ
        isDebug (bool): DEBUG出力するかどうか
    """
    logger = getLogger(isDebug)

    # アクセストークン取得
    with open("../qiita.token", encoding="utf-8") as f:
        global TOKEN
        TOKEN = f.read()

    headers = {
        "Authorization": f'Bearer {TOKEN}',
        "Content-Type": 'application/json'
    }

    # リクエストボディを生成する
    with open("../templete.json", encoding="utf-8") as f:
        item = f.read()
    jsonbody = json.loads(item)

    body = jsonbody["body"]
    for index, event in enumerate(allevents["events"]):
        if index > 4:
            break

        eventname = f'[{event["title"]}]({event["event_url"]})'
        groupname = "" if event["series"] is None else f'[{event["series"]["title"]}]({event["series"]["url"]})'
        accepted = "" if event["accepted"] is None else event["accepted"]
        limit = "" if event["limit"] is None else event["limit"]
        body += f'\n|:{RANKING_EN[index]}:|{eventname}|{groupname}|{accepted}|{limit}|'
        print(f'body={body}')

    jsonbody["body"] = body

    title = jsonbody["title"]
    titledate = enddate.strftime('%Y/%m/%d')
    title = f'{titledate}' + title
    jsonbody["title"] = title

    with open(f'../json/QiitaAPI_requestbody_{enddate}.json', 'w', encoding="utf-8") as f:
        json.dump(jsonbody, f, indent=4)

    requestbody = json.dumps(jsonbody)
    print(f'requestbody={requestbody}')

    try:
        res = requests.post(BASE_URL, headers=headers, json=requestbody)
        print(f'status_code:{res.status_code}, error:{res.text}')
    except Exception as e:
        raise e
