from commonlogger import getLogger, IsDebug
from datetime import date, timedelta
from enum import IntEnum
from typing import Dict, List, Tuple
import copy
import json
import requests

url = "https://connpass.com/api/v1/event/"

class ReportCycle(IntEnum):
    """[summary]
        処理サイクルEnumクラス
    Args:
        Enum ([type]): 処理サイクル
    """
    Dayly = 1
    Weekly = 7
    Monthly = 31

def CallConnpassAPI(eventdate: str, startindex: int = 0) -> Dict:
    """[summary]
    ConnpassAPIを実行し、実行結果をJSONで取得する
    Args:
        eventdate (str): 開催日
        startindex (int): 開始位置 デフォルト0
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

def GetEventData(cycle: ReportCycle, isDebug: bool = False) -> Tuple[date, date, List]:
    """[summary]
    イベントデータを取得する
    Args:
        isDebug (bool): DEBUG出力するかどうか
    Returns:
        (date): 抽出日From
        (date): 抽出日To
        (List): イベントデータ(JSON形式)
    """
    logger = getLogger(isDebug)
    allevents: Dict = {"events": []}
    startdate = None
    enddate = date.today() + timedelta(days=-1)
    logger.debug(f'cycle:{cycle}')
    cycle += 1
    for days in range(1, cycle):
        startdate = date.today() + timedelta(days=(days * -1))
        eventdate = startdate.strftime('%Y%m%d')
        logger.debug(f'days:{days}, eventdate:{eventdate}')

        try:
            events = CallConnpassAPI(eventdate)
            if len(events) == 0:
                print(f'eventdate:{eventdate}, is not events')
                continue
            allevents["events"].extend(events["events"])

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

    sortlist = copy.deepcopy(allevents["events"])
    allevents["events"] = sorted(sortlist, key=lambda x: -x["accepted"])

    if IsDebug():
        outputdate = enddate.strftime('%Y%m%d')
        with open(f'../json/ConnpassAPI_{outputdate}.json', 'w', encoding="utf-8") as f:
            json.dump(allevents, f, indent=4)

    return startdate, enddate, allevents
