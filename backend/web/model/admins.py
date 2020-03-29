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
db = dict_db.Admin.with_options(
    codec_options=CodecOptions(tz_aware=True, tzinfo=local_tz))

# index setting
db.create_index([("name", ASCENDING)], unique=True)
# Default projects for admin
__projection = {'name': 1, 'nick': 1, 'token': 1, 'login_time': 1, 'created_at': 1, 'updated_at': 1}


def save_by_name(admin: dict):
    """
    Save a new admin with field name as index
    :return:
    """
    name = admin.get('name')
    if not name:
        raise Error(10003, 'Field name required!')
    admin['updated_at'] = china_tz(datetime.now())
    admin['created_at'] = china_tz(datetime.now())
    if '_id' in admin:
        del admin['_id']
    entity = db.find_one({'name': name})
    if entity:
        admin['created_at'] = entity['created_at']
        if admin.get('new_password'):
            admin['password'] = sha256_pwd(admin['new_password'], entity['salt'])
            del admin['new_password']
        else:
            admin['password'] = entity.get('password')
        admin['salt'] = entity['salt']
        db.update_one({'_id': entity['_id']}, {
            "$set": admin})
    else:
        admin['salt'] = random_alphanumeric(16)
        if not admin.get('new_password'):
            raise Error(1003, msg='new_password required!')
        admin['password'] = sha256_pwd(admin['new_password'], admin['salt'])
        del admin['new_password']
        db.insert_one(admin)
    return find_by_name(name)


def update_token(entity):
    redis.delete(AUTH_TOKEN_PREFIX + entity.get('token', ''))
    db.update_one({'_id': entity.get('_id')}, {'$set': dict(token=random_alphanumeric(64), login_time=china_tz(datetime.now()))})
    entity = db.find_one({'_id': entity.get('_id')}, __projection)
    redis.setex(AUTH_TOKEN_PREFIX + entity.get('token'), 3600 * 24 * 7, to_json(entity))
    return entity


def login(name: str, password: str):
    entity = db.find_one({'name': name})
    if not entity:
        raise Error(10100)
    password_digest = sha256_pwd(password, entity.get('salt'))
    if password_digest != entity.get('password'):
        raise Error(10101)
    return update_token(entity)


def logout(token: str):
    admin = redis.get(AUTH_TOKEN_PREFIX + token)
    if admin:
        admin = parse_json(admin)
        db.update_one({'_id': admin.get('_id')}, {'$set': dict(token='', updated_at=china_tz(datetime.now()))})
    redis.delete(AUTH_TOKEN_PREFIX + token)


def init():
    if not db.find_one({'name': 'admin'}, __projection):
        save_by_name(dict(name='admin', nick='诛仙', new_password='111111'))


def find_fuzzy(keyword: str, skip: int, limit: int):
    regex = re.compile(keyword, re.IGNORECASE)
    sorts = [("updated_at", DESCENDING), ("created_at", DESCENDING)]
    result = db.find({'$or': [{'name': regex}, {'nick': regex}, {'token': regex}]}, __projection).sort(
        sorts).skip(skip).limit(limit)
    return list(result)


def find_by_name(name: str):
    return db.find_one({'name': name}, __projection)


def find_by_id(_id: str):
    return db.find_one({'_id': ObjectId(_id)}, __projection)


def delete_by_id(_id: str):
    result = db.delete_one({'_id': ObjectId(_id)}).raw_result
    log.info('Delete document: %s | %s', _id, result)
    return result


# init data
init()
