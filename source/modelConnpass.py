from commonlogger import getLogger, IsDebug
from datetime import date
from datetime import timedelta
from typing import Dict
import json
import requests

url = "https://connpass.com/api/v1/event/"


def CallConnpassAPI(eventdate: str, startindex: int = 0) -> Dict:
    """[summary]
    ConnpassAPIを実行し、実行結果をJSONで取得する
    Args:
        eventdate (str): 開催日
        startindex (int): 開始位置　デフォルト0
    Returns:
        (dict): 実行結果
    """
    params = {
        'ymd': eventdate,
        'count': 100,
        'order': 2
    }
    if startindex > 0:
        params['start'] = startindex

    try:
        responce = requests.get(url, params=params)
        result_json = responce.json()
        return result_json
    except Exception as e:
        print('Error code: ', e.code)
        raise e


def GetEventData(isDebug: bool = False) -> Dict:
    """[summary]
    イベントデータを取得する
    Args:
        isDebug (bool): DEBUG出力するかどうか
    Returns:
        (dict): イベントデータ(JSON形式)
    """
    logger = getLogger(isDebug)
    allevents: Dict = {"events": []}
    outputdate = date.today().strftime('%Y%m%d')
    for days in range(0, 1):
        targetDate = date.today()

        if days > 0:
            targetDate += timedelta(days=(days * -1))
        eventdate = targetDate.strftime('%Y%m%d')
        logger.debug(f'days:{days}, eventdate:{eventdate}')

        try:
            events = CallConnpassAPI(eventdate)
            if len(events) == 0:
                print(f'eventdate:{eventdate}, is not events')
                continue

            if len(allevents["events"]) == 0:
                allevents["events"] = events["events"]
            else:
                allevents["events"].append(events["events"])

            results_start = events["results_start"]
            results_returned = events["results_returned"]
            results_available = events["results_available"]
            logger.debug(
                f'count:{len(events)}, results_start:{results_start}, results_returned:{results_returned}, results_available:{results_available}')

            while results_returned == 100 and results_available > 100:
                results_start += 100
                events_next = CallConnpassAPI(eventdate, results_start)
                results_start = events_next["results_start"]
                results_returned = events_next["results_returned"]
                results_available = events_next["results_available"]
                logger.debug(
                    f'count:{len(events_next)}, results_start:{results_start}, results_returned:{results_returned}, results_available:{results_available}')
                for event_next in events_next["events"]:
                    allevents["events"].append(event_next)
        except Exception as e:
            if type(e) == ValueError:
                pass
            else:
                raise e

        allevents = sorted(allevents["events"], key=lambda x: -x["accepted"])

        if IsDebug():
            with open(f'../json/ConnpassAPI_{outputdate}.json', 'w', encoding="utf-8") as f:
                json.dump(allevents, f, indent=4)