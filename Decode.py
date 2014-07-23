#!/usr/bin/python2

class DecodeError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

escapes = {
        "n": "\n",
        "t": "\t",
        "v": "\v",
        "b": "\b",
        "v": "\v",
        "f": "\f",
        "r": "\r",
        "a": "\a",
        "\\": "\\",
        "\"": "\"",
        "'": "'",
        } 

def decode(text):
    def decodeString(iterable):
        value = ""
        for char in iterable:
            if char == "\\":
                value += escapes.get(next(iterable), "\\")
                continue
            value += char
        return value

    obj = {}
    for line in text.splitlines():
        key, separator, value = line.partition(": ")
        if not separator:
            raise DecodeError("No separator on line {!r}".format(line))
        obj[key] = decodeString(iter(value))

    return obj

