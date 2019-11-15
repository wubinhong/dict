from datetime import datetime
from pymongo import ASCENDING
from web.util import china_tz, local_tz
from web.flask import dict_db
from bson.codec_options import CodecOptions

# 配置datetime时区
word_collection = dict_db.Word.with_options(
    codec_options=CodecOptions(tz_aware=True, tzinfo=local_tz))

# index setting
word_collection.create_index([("name", ASCENDING)], unique=True)
word_collection.create_index([("derivation", ASCENDING)])


def save(name: str, derivation=None, chinese=None, thesauri=None, related_words=None,
         similar_shaped_words=None):
    """
    Save a new word with field name as index
    :param name: 单词
    :param derivation: 词根组成，如：a+scend
    :param chinese: 中文解释，多种解释使用逗号（,）分隔
    :param thesauri: 同义词，使用逗号（,）分隔
    :param related_words: 相关单词，使用逗号（,）分隔
    :param similar_shaped_words: 形状相识的单词，使用逗号（,）分隔
    :return:
    """
    new_word = dict(name=name, derivation=derivation, chinese=chinese, thesauri=thesauri, related_words=related_words,
                    similar_shaped_words=similar_shaped_words, created_at=china_tz(datetime.now()))
    w = word_collection.find_one({'name': name})
    if w:
        new_word['created_at'] = w['created_at']
        word_collection.update_one({'name': name}, {
            "$set": new_word})
    else:
        word_collection.insert_one(new_word)
    return new_word


def find_fuzzy(keyword: str, skip: int, limit: int):
    result = word_collection.find({'$or': [{'name': {'$regex': keyword}}, {'derivation': {'$regex': keyword}},
                                           {'chinese': {'$regex': keyword}}, {'thesauri': {'$regex': keyword}},
                                           {'related_words': {'$regex': keyword}},
                                           {'similar_shaped_words': {'$regex': keyword}}]}).skip(skip).limit(limit)
    return list(result)
