from commonlogger import getLogger, IsDebug
from datetime import date
from typing import Dict
import json
import requests

BASE_URL = "https://qiita.com/api/v2/items"
TOKEN = ""


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
    with open("./qiita.token", encoding="utf-8") as f:
        global TOKEN
        TOKEN = f.read()
    # print(f'TOKEN:{TOKEN}')
    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json"
    }

    # リクエストボディを生成する
    with open("./templete.json", encoding="utf-8") as f:
        item = f.read()
    requestbody = json.loads(item)

    body = requestbody["body"]
    for index, event in enumerate(allevents["events"]):
        if index > 4:
            break

        rank = (index + 1)
        eventname = f'[{event["title"]}]({event["event_url"]})'
        groupname = f'[{event["series"]["title"]}]({event["series"]["url"]})'
        accepted = "" if event["accepted"] == "None" else event["accepted"]
        limit = "" if event["limit"] == "None" else event["limit"]
        body += f'|:{rank}:|{eventname}|{groupname}|{accepted}|{limit}|'
    requestbody["body"] = body

    title = requestbody["title"]
    titledate = enddate.strftime('%Y/%m/%d')
    title = f'{titledate}' + title
    requestbody["title"] = title

    print(requestbody)

    try:
        res = requests.post(BASE_URL, headers=headers, json=body)
        print(f'status_code:{res.status_code}, error:{res.text}')
    except Exception as e:
        raise e
