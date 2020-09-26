from datetime import datetime

from bson import json_util, ObjectId
from bson.codec_options import CodecOptions
from pymongo import ASCENDING, DESCENDING

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
        raise Error(10003, 'Field name required!')
    updated_time_on = word.get('updated_time_on')
    if 'updated_time_on' in word:
        del word['updated_time_on']
    if '_id' in word:
        del word['_id']
    w = word_collection.find_one({'name': name})
    if w:
        word['created_at'] = w['created_at']
        if updated_time_on:
            word['updated_at'] = china_tz(datetime.now())
        else:
            word['updated_at'] = w['updated_at']
        word_collection.update_one({'_id': w['_id']}, {
            "$set": word})
    else:
        word['updated_at'] = china_tz(datetime.now())
        word['created_at'] = china_tz(datetime.now())
        word_collection.insert_one(word)
    return word


def find_fuzzy(keyword: str, skip: int, limit: int):
    regex = re.compile(keyword, re.IGNORECASE)
    sorts = [("hardship", DESCENDING), ("updated_at", DESCENDING)]
    result = word_collection.find({'$or': [{'name': regex}, {'derivation': regex},
                                           {'chinese': regex}, {'thesauri': regex}, {'related_words': regex},
                                           {'similar_shaped_words': regex}, {'comment': regex}]}).sort(sorts).skip(skip).limit(limit)
    return list(result)


def find_by_name(name: str):
    return word_collection.find_one({'name': name})


def delete_by_name(name: str):
    result = word_collection.delete_one({'name': name}).raw_result
    log.info('Delete document: %s | %s', name, result)
    return result


def delete_by_id(_id: str):
    result = word_collection.delete_one({'_id': ObjectId(_id)}).raw_result
    log.info('Delete document: %s | %s', _id, result)
    return result
