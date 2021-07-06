from commonlogger import getLogger, IsDebug
from datetime import date
from qiita_v2.client import QiitaClient
from typing import Dict
import json
import requests

BASE_URL = "https://qiita.com/api/v2/items"
RANKING_EN = ["one", "two", "three", "four", "five"]


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
    token = None
    with open("../qiita.token", encoding="utf-8") as f:
        token = f.read()

    client = QiitaClient(access_token=token)

    # リクエストボディを生成する
    with open("../templete.json", encoding="utf-8") as f:
        item = f.read()
    jsonbody = json.loads(item)

    body = jsonbody["body"]
    for index, event in enumerate(allevents["events"]):
        if index > 4:
            break

        eventname = f'[{event["title"]}]({event["event_url"]})'
        groupname = "" if event[
            "series"] is None else f'[{event["series"]["title"]}]({event["series"]["url"]})'
        accepted = "" if event["accepted"] is None else event["accepted"]
        limit = "" if event["limit"] is None else event["limit"]
        bodyline = f'\n|:{RANKING_EN[index]}:|{eventname}|{groupname}|{accepted}|{limit}|'
        body += bodyline
        logger.debug(
            f'eventname={eventname}, groupname={groupname}, accepted={accepted}, limit={limit}')
        logger.debug(f'bodyline={bodyline}')

    jsonbody["body"] = body

    title = jsonbody["title"]
    titledate = enddate.strftime('%Y/%m/%d')
    title = f'{titledate}' + title
    jsonbody["title"] = title
    logger.debug(f'body={jsonbody}')

    with open(f'../json/QiitaAPI_requestbody_{enddate}.json', 'w', encoding="utf-8") as f:
        json.dump(jsonbody, f, indent=4)

    try:
        res = client.create_item(params=jsonbody)
        print(res)
    except Exception as e:
        raise e
