from flask import Flask
from datetime import datetime
import time

app = Flask(__name__)


@app.route('/')
def hello_world():
    now = datetime.now()
    ts = int(now.timestamp())
    print('Access: %s | %s' % (now, now.timestamp()))
    if ts % 2 == 0:     # 模拟服务不健康的情况，测试docker的 HEALTHCHECK 指令
        print('Even number for ts, system will sleep for 10 sec: %s' % ts)
        time.sleep(10)
    return 'Flask Dockerized: %s' % now


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')