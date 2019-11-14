from datetime import datetime
from unittest import TestCase

from bson import json_util

from util import get_logger
from web.model import words

log = get_logger(__name__)


class TestWebModelWord(TestCase):
    def test_save(self):
        words.save(name='ascend', derivation='a+scend', chinese='上升, 促进22', thesauri='up, lift', related_words='',
                   similar_shaped_words='descend')
        words.save(name='descend', derivation='de+scend', chinese='下降', thesauri='down', related_words='',
                   similar_shaped_words='descend')
        words.save(name='transcend', derivation='tran+scend', chinese='胜过, 超越', thesauri='surpass, excel',
                   related_words='',
                   similar_shaped_words='descend')
        words.save(name='offspring', chinese='后代', thesauri='descendant')

    def test_find_fuzzy(self):
        keyword = 'cend'
        log.info('find fuzzy: %s | %s', keyword, json_util.dumps(words.find_fuzzy(keyword, 0, 3), indent=1))
