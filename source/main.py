from commonlogger import getLogger
from modelConnpass import GetEventData
from modelQiita import PostQiita
import sys


if __name__ == "__main__":

    isDebug = (len(sys.argv) > 1)
    # ロギング
    logger = getLogger(isDebug)

    # ConnpassAPIよりイベントデータを取得する
    startdate, enddate, allevents = GetEventData(isDebug)

    # イベントデータをQiitaに送信する
    PostQiita(startdate, enddate, allevents, isDebug)
