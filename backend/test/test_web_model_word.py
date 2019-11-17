from unittest import TestCase

from bson import json_util

from web.util import get_logger
from web.model import words

log = get_logger(__name__)


class TestWebModelWord(TestCase):
    """
    Test case for model word
    """

    def test_save(self):
        log.info('Test save start...')
        words.save(dict(name='ascend', derivation='a+scend', chinese='上升, 促进22',
                        thesauri='up, lift', similar_shaped_words='descend'))
        words.save(dict(name='descend', derivation='de+scend',
                        chinese='下降', thesauri='down', similar_shaped_words='descend'))
        words.save(dict(name='transcend', derivation='tran+scend', chinese='胜过, 超越',
                        thesauri='surpass, excel', similar_shaped_words='descend'))
        words.save(dict(name='offspring', chinese='后代', thesauri='descendant'))

    def test_find_fuzzy(self):
        keyword = 'cend'
        log.info('find fuzzy: %s | %s', keyword, json_util.dumps(
            words.find_fuzzy(keyword, 0, 3), indent=1))
