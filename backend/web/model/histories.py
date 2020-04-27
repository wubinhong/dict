import re
from datetime import datetime

from bson import ObjectId
from bson.codec_options import CodecOptions
from pymongo import ASCENDING, DESCENDING

from web.flask import dict_db, redis
from web.setting import AUTH_TOKEN_PREFIX
from web.util import china_tz, get_logger, local_tz, random_alphanumeric, to_json, parse_json, sha256_pwd
from web.util.error import Error

log = get_logger(__file__)
# 配置datetime时区
db = dict_db.History.with_options(
    codec_options=CodecOptions(tz_aware=True, tzinfo=local_tz))

# index setting
db.create_index([("title", ASCENDING)], unique=True)
# Default projects for history
__projection = {'_id': 1, 'title': 1,
                'content': 1, 'created_at': 1, 'updated_at': 1}


def save_by_title(history: dict):
    """
    Save a new history with field title as index
    :return:
    """
    title = history.get('title')
    if not title:
        raise Error(10003, 'Field title required!')
    history['updated_at'] = china_tz(datetime.now())
    history['created_at'] = china_tz(datetime.now())
    if '_id' in history:
        _id = ObjectId(history['_id'])
        del history['_id']
        del history['created_at']
        db.update_one({'_id': _id}, {
            "$set": history})
        return find_by_title(title)
    entity = db.find_one({'title': title})
    if entity:
        history['created_at'] = entity['created_at']
        db.update_one({'_id': entity['_id']}, {
            "$set": history})
    else:
        db.insert_one(history)
    return find_by_title(title)


def find_fuzzy(keyword: str, skip: int, limit: int):
    regex = re.compile(keyword, re.IGNORECASE)
    sorts = [("title", DESCENDING), ("created_at", DESCENDING)]
    result = db.find({'$or': [{'content': regex}]}, __projection).sort(
        sorts).skip(skip).limit(limit)
    return list(result)


def find_by_title(title: str):
    return db.find_one({'title': title}, __projection)


def delete_by_id(_id: str):
    result = db.delete_one({'_id': ObjectId(_id)}).raw_result
    log.info('Delete document: %s | %s', _id, result)
    return result


def find_by_id(id: str):
    return db.find_one({'_id': ObjectId(id)}, __projection)
