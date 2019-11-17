from unittest import TestCase

from bson import json_util

from web.util import get_logger
from web.model import words

log = get_logger(__name__)


class TestModelWords(TestCase):

    def test_delete_by_name(self):
        log.info('Test delete document by name: %s', words.delete_by_name('kkk'))
