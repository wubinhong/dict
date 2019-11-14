class Error(Exception):
    MAPS = {
        10000: "income parameters error",
        10001: "project not exists.",
        10002: "host not exists.",
        10003: "user not exists.",
        10004: "deploy permission denied.",
        10005: "Incomplete parameter",
        # live module
        10100: "Fail to just live channel time"
    }

    def __init__(self, code, msg=None):
        self.code = code
        if msg is None:
            self.msg = self.MAPS[code]
        else:
            self.msg = msg

    def __repr__(self):
        return "%s: %s" % (self.code, self.msg)
