from commonlogger import getLogger
from modelConnpass import GetEventData, ReportCycle
from modelQiita import PostQiita
import base64
import sys

def run_pubsub(event, context):
    print("EventReportPage start")
    main()
    print("EventReportPage finish")

def test_pubsub(event, context):
    """Triggered from a message on a Cloud Pub/Sub topic.
    Args:
         event (dict): Event payload.
         context (google.cloud.functions.Context): Metadata for the event.
    """
    print("pub/sub forwarded")
    pubsub_message = base64.b64decode(event['data']).decode('utf-8')
    print(pubsub_message)

def main():

    isDebug = (len(sys.argv) > 1)
    # ロギング
    logger = getLogger(isDebug)

    # ConnpassAPIよりイベントデータを取得する
    startdate, enddate, allevents = GetEventData(ReportCycle.Dayly, isDebug)

    # イベントデータをQiitaに送信する
    PostQiita(startdate, enddate, allevents, isDebug)

if __name__ == "__main__":
    main()
