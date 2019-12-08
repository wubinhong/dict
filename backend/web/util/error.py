class Error(Exception):
    MAPS = {
        10000: "Header x-hucat-token required!",
        10001: "Login required!",
        10002: "Income parameters error",
        10003: "Lack of required parameter.",
        # admin module
        10100: "管理员不存在",
        10101: "用户名、密码不匹配"
    }

    def __init__(self, rc, msg=None):
        self.rc = rc
        if msg is None:
            self.msg = self.MAPS[rc]
        else:
            self.msg = msg

    def __repr__(self):
        return "%s: %s" % (self.rc, self.msg)
