import logging
import os
from logging.handlers import TimedRotatingFileHandler

from const import LOG_DIR


class FunctionalTestsLogger(logging.Logger):

    def critical(self, msg, *args, **kwargs):
        super(FunctionalTestsLogger, self).critical(msg, *args, **kwargs)
        raise Exception(msg)


logging.setLoggerClass(FunctionalTestsLogger)
logger = logging.getLogger(FunctionalTestsLogger.__name__)
logger.setLevel(logging.DEBUG)

LOG_FMT = logging.Formatter("%(asctime)s  %(filename)-24s[:%(lineno)-4d]  %(levelname)-8s  %(message)s")

# log by day
# fh = TimedRotatingFileHandler(
#     filename=os.path.join(LOG_DIR, f'{datetime.datetime.now().strftime("%Y%m%d")}.log'),
#     when="MIDNIGHT",
#     encoding='utf-8')
fh = TimedRotatingFileHandler(
    filename=os.path.join(LOG_DIR, 'it-log'),
    when="MIDNIGHT",
    encoding='utf-8')

fh.setLevel(logging.DEBUG)
fh.setFormatter(LOG_FMT)
logger.addHandler(fh)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(LOG_FMT)
logger.addHandler(ch)
logging.basicConfig()