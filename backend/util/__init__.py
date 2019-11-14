import logging

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

