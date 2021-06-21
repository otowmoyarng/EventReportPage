import logging


def getLogger(isDebug: bool = False) -> logging.Logger:
    """[summary]
        ロガーを初期化する
    Args:
        isDebug (bool): DEBUG出力するかどうか
    Returns:
        logging.Logger: ロガー
    """
    logger = logging.getLogger('EventReportPage')
    if isDebug:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)
    return logger


def IsDebug() -> bool:
    """[summary]
        ログレベルがDEBUGかどうか
    Returns:
        bool: true/false
    """
    return logging.getLogger().level == logging.DEBUG
