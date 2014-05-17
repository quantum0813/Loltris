#!/usr/bin/python

def rgbHexDecode(s):
    """
    >>> rgbHexDecode("#FFFFFF")
    (255, 255, 255)
    >>> rgbHexDecode("#f4f4f4")
    (244, 244, 244)
    >>> rgbHexDecode("FFFFFF")
    (255, 255, 255)
    """
    s = s.upper()
    if s[0] == "#":
        s = s[1:]
    return (int(s[0:2], 16), int(s[2:4], 16), int(s[4:6], 16))

def rgbHexEncode(rgb):
    """
    >>> rgbHexEncode((0xff,0xff,0xff))
    '#FFFFFF'
    """
    def hexByte(num):
        if num > 255 or num < 0:
            raise TypeError("Each number must be in range [0, 255], got `{}'".format(rgb))
        if num >= 10:
            return hex(num)[2:].upper()
        return "0" + hex(num)[2:].upper()
    return "#" + "".join([hexByte(byte) for byte in rgb])

if __name__ == '__main__':
    import doctest
    doctest.testmod()
