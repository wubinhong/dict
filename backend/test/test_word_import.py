import re
from datetime import datetime
from os.path import dirname, join, realpath
from unittest import TestCase

from bson import json_util
from pymongo import MongoClient

from web.model import words
from web.setting import MONGO_URI
from web.util import china_tz, get_logger

log = get_logger(__name__)


class TestWordImport(TestCase):

    def setUp(self):
        log.info('Db init start...')
        self.db = MongoClient(MONGO_URI, tz_aware=True)['dict']

    def handle_comma_str(self, comma_str: str):
        """
        处理带逗号的字符串，如：
        bull, luxury, , , plugins, critic, --> bull, luxury, plugins, critic
        """
        comma_str = comma_str.strip()
        comma_list = list(v.strip() for v in comma_str.split(',') if v.strip())
        return ', '.join(comma_list)

    def handle_other(self, word_detail):
        """
        Example:
        plugins, critic, 相关: bull, luxury, 形: hall, hallway
        """
        word = {}
        for r in re.findall(r'相关:[a-z ,]+', word_detail):
            word_detail = word_detail.replace(r, '')
            word['related_words'] = re.findall(r'相关:([a-z ,]+)', r)[0].strip()
        for r in re.findall(r'形:[a-z ,]+', word_detail):
            word_detail = word_detail.replace(r, '')
            word['similar_shaped_words'] = re.findall(r'形:([a-z ,]+)', r)[0].strip()
        word['thesauri'] = ', '.join(word_detail.split(','))
        return word

    def handle_line(self, line_number, sample: str):
        # 具体的处理逻辑
        return_words = []
        log.info('Handle line:\n---\n%s: %s\n---', line_number, sample)
        # ansi字符开头，后面紧跟一个括号()，括号里由英文字母、逗号、->、空格还有汉字组成
        # 处理带词根的，如 immense(im men(measure，测量)+se->, plugins, critic, 相关: bull, luxury, 形: hall, hallway)
        for m in re.findall(r'\w+\([\w, +()，]*->, [\w, :]*\)', sample):
            sample = sample.replace(m, '')  # Remove matched str
            # Handle match str: a new word with more detail
            # Generally speaking there will be just one element in this case
            for m_g in re.findall(r'(\w+)\(([\w, +()，]*)->, ([\w, :]*)\)', m):
                word = {'name': m_g[0].strip(), 'derivation': m_g[1], **self.handle_other(m_g[2])}
                log.debug('Complicated bulk word analyze result: %s', word)
                return_words.append(word)
        for w in sample.split(','):
            w = w.replace(' ', '').replace('\n', '')
            if w:   # 过虑掉前面处理过的单词
                return_words.append(dict(name=w))
        log.debug('Add other simple word: %s', return_words)
        return return_words

    def upgrade_poor_format(self, sample):
        """
        For example: insulate, ethical(moral), ethnic(ethnical, racial, 形: ethic, ethic2), evenly(equally->, poor, good)
        --> insulate, ethical(->, moral), ethnic(->, ethnical, racial, 形: ethic, ethic2), evenly(equally->, poor, good)
        Just to make a format for method @handle_line
        """
        # sample = 'insulate, ethical(moral), ethnic(ethnical, racial, 形: ethic, ethic2), evenly(equally->, poor, good)'
        # 以", "，或者回车"\n"结尾
        for m in re.findall(r'\w+\([\w ,:]+\)(?:, |\n)', sample):
            for m_g in re.findall(r'(\w+\()([\w ,:]+\)(?:, |\n))', m):
                new_str = m_g[0] + '->, ' + m_g[1]
                sample = sample.replace(m, new_str)
        log.info('Sample upgraded: %s', sample)
        return sample

    def test_regex(self):
        regex = re.compile(r'\d+\.\d*')
        regex_start_with_ch = re.compile(r'\w.+')
        log.debug('first: %s', regex.search('asdf23.35fasdkl0.2382asdfas222dsfald'))
        log.debug('second: %s', regex_start_with_ch.match('---'))
        log.debug('tem test: %s', re.findall(r'(\d+)\.(\d*)', 'asdf23.35fasdkl0.2382asdfas222dsfald'))
        ex_str = 'imitate, immense(im men(measure，测量)+se->, plugins, critic, 相关: bull, luxury, 形: hall, hallway), impetus, immense1(im men(measure，测量)+se->, ), immense2(kevin, lucy, 相关: sam, 形: coco)'
        # 处理带词根的
        re.findall(r'\w+\([\w, +()，]+->, [\w, :]*\)', ex_str)
        re.findall(r'(\w+)\(([\w, +()，]+)->, ([\w, :]*)\)', ex_str)    # 加分组
        # 处理不带词根的
        ex_str = 'imitate, immense(im men(measure)+se->, plugins), impetus, immense2(kevin, plugins, critic, 相关: bull, luxury, 形: hall, hallway)'
        re.findall(r'\w+\([\w, +]*\)', ex_str)
        re.findall(r'(\w+)\(([\w, +]*)\)', ex_str)
        # sample = 'jack, peer(dd->, aa->, bb, cc), couple, cradle, culminate(climax, peak, 形: accumulate), urban(metropolitan, civic, 相关: rural, suburb, exurban), critic '
        # sample = 'imaginative, imbalance, imitate, immense(im+men(measure)+se->, ), immerse(im+merse(merge)->, ), immigrant(im+migr(move)+ant->, ), impede(im+pede(foot)->, hinder), impetus(im+pet(拍打)+us->, 同词根: perpetuate), impress, impulse(im(onto)+pul(push)+se->, )'
        sample = 'committee(commission), compost, compromise, comprise, compulsory(obligatory, mandatory), communal(community->, public), compelling, concrete(specific, material)\n'
        # log.info('EE2:%s', self.handle_comma_str('     bull, luxury, , , plugins, critic, '))
        # log.info('EE: %s', self.handle_other('plugins,      critic, 相关: bull, luxury, 形: hall, hallway'))
        line = self.upgrade_poor_format(sample)
        log.info('Line handle result:\n<---\n%s\n<---', json_util.dumps(self.handle_line(1, line)))

    def test_import(self):
        word_coll = self.db.Word
        log.info('word_coll: %s', word_coll)
        file = join(dirname(realpath(__file__)), 'seeds', 'data_word.txt')
        with open(file, 'r', encoding='utf-8') as f:
            for i, line in enumerate(f):
                if re.search(r'^\w+', line):  # 单词行
                    ret_words = self.handle_line(i + 1, self.upgrade_poor_format(line))
                    if ret_words:
                        for w in ret_words:
                            w_db = word_coll.find_one({'name': w.get('name')})
                            if not w_db:
                                w['created_at'] = china_tz(datetime.now())
                                # Remove fields with None value by constructing a new dict only having field with concrete value.
                                word_coll.insert_one({k: v for k, v in w.items() if v})
