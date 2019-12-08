import datetime
import logging
import random as __random
import string
from hashlib import sha256 as __sha256

import pytz
from bson import json_util

local_tz = pytz.timezone('Asia/Shanghai')

FORMAT = '%(asctime)s %(levelname)s %(process)d -- [%(threadName)s] [%(name)s:%(lineno)s] : %(message)s'


def get_logger(name: str):
    """
    Construct a logger based on python logging module
    :param name: logger category name, generally mean the python module full name, e.g. web.rest.dict
    :return:
    """
    logger = logging.getLogger(name)
    if len(logger.handlers):    # Mean the specified logger has been init, so just return
        return logger
    # 基础，决定后面的sh能过滤哪个级别的信息
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter(FORMAT)
    sh = logging.StreamHandler()
    sh.setFormatter(formatter)
    sh.setLevel(logging.DEBUG)
    logger.addHandler(sh)
    return logger


def right_just_dict(obj: dict, width=20) -> str:
    """
    对对象属性进行字符串格式化，中间对其
    :param obj: pojo对象
    :param width: 右对齐需要padding的宽度
    :return: 格式化后的字符串
    """
    result = ''
    for k, v in obj.items():
        result += '{} : {}\n'.format(str(k).rjust(width), v)
    return result.strip('\n')


def china_tz(dt: datetime) -> datetime:
    """
    返回东八区的中国时间
    :param dt:
    :return:
    """
    if dt.tzinfo is not None:
        return dt.astimezone(local_tz)
    return local_tz.localize(dt, is_dst=None)


def make_msg(rc: int = 0, data=None, msg: str = 'Response success!') -> dict:
    return dict(rc=rc, data=data, msg=msg, ts=datetime.datetime.now().timestamp())


def random(count: int, letters: bool, numbers: bool, seed=''):
    if letters:
        seed += string.ascii_uppercase + string.ascii_lowercase
    if numbers:
        seed += string.digits
    return ''.join(__random.choices(seed, k=count))


def random_alphanumeric(count=16):
    return random(count, True, True)


def to_json(obj: dict) -> str:
    return json_util.dumps(obj)


def parse_json(obj: str) -> dict:
    return json_util.loads(obj)


def sha256_pwd(password: str, salt: str):
    """
    sha256算法加密密码
    """
    return __sha256((password + salt).encode(encoding='utf-8')).hexdigest()
