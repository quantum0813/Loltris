#!/usr/bin/python2

class EncodeError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

CONTORL_CHARACTERS = set([chr(c) for c in xrange(0x20)])
def encode(obj):
    text = ""
    for key in obj:
        if any(c in CONTORL_CHARACTERS.union({":"}) for c in key):
            raise EncodeError("Invalid characters in key {!r}".format(key))
        if not isinstance(obj[key], str):
            raise EncodeError("Non-string value {!r}".format(obj[key]))
        if not isinstance(key, str):
            raise EncodeError("Non-string key {!r}".format(key))
        text += "{}: {}\n".format(key, repr(obj[key])[1:-1])
    return text

