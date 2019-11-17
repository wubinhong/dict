class Error(Exception):
    MAPS = {
        10000: "Income parameters error",
        10001: "Lack of required parameter.",
        # user module
        10100: "Fail to xxx"
    }

    def __init__(self, code, msg=None):
        self.code = code
        if msg is None:
            self.msg = self.MAPS[code]
        else:
            self.msg = msg

    def __repr__(self):
        return "%s: %s" % (self.code, self.msg)
