import logging
import time
from datetime import datetime

from flask import Flask

FORMAT = '%(asctime)s %(levelname)s %(process)d -- [%(threadName)s] [%(name)s:%(lineno)s] : %(message)s'

app = Flask(__name__)


def get_logger(name: str):
    logger = logging.getLogger(name)
    # 基础，决定后面的sh能过滤哪个级别的信息
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter(FORMAT)
    sh = logging.StreamHandler()
    sh.setFormatter(formatter)
    sh.setLevel(logging.DEBUG)
    logger.addHandler(sh)
    return logger

log = get_logger('app')


@app.route('/')
def hello_world():
    now = datetime.now()
    ts = int(now.timestamp())
    # 注意: 使用控制台打印的信息也会输出到docker的标准in/out上，也可以通过 docker logs命令查看到，但是数据不是实时更新的
    print('Console Access: %s | %s' % (now, now.timestamp()))
    log.info('Logger Access: %s | %s', now, now.timestamp())
    if ts % 8 == 0:     # 模拟服务不健康的情况，测试docker的 HEALTHCHECK 指令，2/8的几率不健康
        print('Even number for ts, system will sleep for 10 sec: %s' % ts)
        time.sleep(6)
    return 'Flask Dockerized: %s' % now


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')