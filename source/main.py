from modelConnpass import GetEventData
from commonlogger import getLogger
import sys


if __name__ == "__main__":

    isDebug = (len(sys.argv) > 1)
    # ロギング
    logger = getLogger(isDebug)

    # ConnpassAPIよりイベントデータを取得する
    allevents = GetEventData(isDebug)

    print('postqiita')
