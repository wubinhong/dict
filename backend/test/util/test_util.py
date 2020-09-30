from datetime import datetime
from unittest import TestCase

import pytz
from bson import json_util
from web.model import words
from web.util import china_tz, get_logger

log = get_logger(__name__)


class TestUtil(TestCase):
    """
    Test case for model word
    """

    def test_datetime(self):
        log.info('Test datetime start...')
        # log.info('tzs: %s', pytz.all_timezones)
        # Asia/Tokyo
        tokyo = pytz.timezone('Asia/Tokyo')
        cn = pytz.timezone('Asia/Shanghai')
        n = datetime.now()
        log.info('tz: %s', tokyo)
        log.info('tzinfo: %s', n.tzinfo)
        log.info('tzinfo.astimezone: %s', n.astimezone(tokyo).tzinfo)
        log.info('astimezone.tokyo: %s', n.astimezone(tokyo))
        log.info('astimezone.cn: %s', n.astimezone(cn))
        log.info('localize.tokyo: %s', tokyo.localize(n, is_dst=None))
        log.info('localize.cn: %s', cn.localize(n, is_dst=None))
        log.info('china_tz: %s', china_tz(n))

        log.info('tzinfo.astimezone astimezone astimezone astimezone astimezone astimezone astimezone astimezone: %s',
                 n.astimezone(tokyo).tzinfo)
