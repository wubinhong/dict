from datetime import datetime

from bson import json_util
from bson.codec_options import CodecOptions
from pymongo import ASCENDING

from web.flask import dict_db
from web.util import china_tz, get_logger, local_tz
from web.util.error import Error
import re

log = get_logger(__file__)
# 配置datetime时区
word_collection = dict_db.Word.with_options(
    codec_options=CodecOptions(tz_aware=True, tzinfo=local_tz))

# index setting
word_collection.create_index([("name", ASCENDING)], unique=True)
word_collection.create_index([("derivation", ASCENDING)])


def save(word: dict):
    """
    Save a new word with field name as index
    :return:
    """
    name = word.get('name')
    if not name:
        raise Error(10001, 'Field name required!')
    word['created_at'] = china_tz(datetime.now())
    w = word_collection.find_one({'name': name})
    if w:
        if '_id' in word:
            del word['_id']
        word['created_at'] = w['created_at']
        word_collection.update_one({'_id': w['_id']}, {
            "$set": word})
    else:
        word_collection.insert_one(word)
    return word


def find_fuzzy(keyword: str, skip: int, limit: int):
    regex = re.compile(keyword, re.IGNORECASE)
    result = word_collection.find({'$or': [{'name': regex},
                                           {'derivation': regex},
                                           {'chinese': regex}, {
                                               'thesauri': regex},
                                           {'related_words': regex}, {'similar_shaped_words': regex}]}).skip(skip).limit(limit)
    return list(result)


def delete_by_name(name: str):
    result = word_collection.delete_one({'name': name}).raw_result
    log.info('Delete document: %s | %s', name, result)
    return result
