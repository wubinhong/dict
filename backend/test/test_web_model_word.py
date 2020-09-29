from unittest import TestCase

from bson import json_util

from web.util import get_logger
from web.model import words

log = get_logger(__name__)


class TestWebModelWord(TestCase):
    """
    Test case for model word
    """

    def test_add(self):
        log.info('Test save start...')
        if not words.find_by_name('ascend'):
            words.add(dict(name='ascend', derivation='a+scend', chinese='上升, 促进22',
                           thesauri='up, lift', similar_shaped_words='descend'))
        if not words.find_by_name('descend'):
            words.add(dict(name='descend', derivation='de+scend',
                           chinese='下降', thesauri='down', similar_shaped_words='descend'))
        if not words.find_by_name('transcend'):
            words.add(dict(name='transcend', derivation='tran+scend', chinese='胜过, 超越',
                           thesauri='surpass, excel', similar_shaped_words='descend'))
        if not words.find_by_name('offspring'):
            words.add(dict(name='offspring', chinese='后代', thesauri='descendant'))

    def test_find_fuzzy(self):
        keyword = 'cend'
        log.info('find fuzzy: %s | %s', keyword, json_util.dumps(
            words.find_fuzzy(keyword, 0, 3), indent=1))
