from commonlogger import getLogger
from modelConnpass import GetEventData, ReportCycle
from modelQiita import PostQiita
import sys


if __name__ == "__main__":

    isDebug = (len(sys.argv) > 1)
    # ロギング
    logger = getLogger(isDebug)

    # ConnpassAPIよりイベントデータを取得する
    startdate, enddate, allevents = GetEventData(ReportCycle.Dayly, isDebug)

    # イベントデータをQiitaに送信する
    PostQiita(startdate, enddate, allevents, isDebug)
