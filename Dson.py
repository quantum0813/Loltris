#!/usr/bin/python2
#-*- coding: utf-8 -*-

## =====================================================================
## DSON parser/serializer for Python2
## Copyright (C) 2014 Jonas Møller <shrubber@tfwno.gf>
##
## This program is free software: you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation, either version 3 of the License, or
## (at your option) any later version.
##
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with this program.  If not, see <http://www.gnu.org/licenses/>.
## =====================================================================

from pprint import pprint
from copy import copy

constants = {
        "yes": True,
        "no": False,
        "empty": None,
        }
constants_reverse = {
        True: "yes",
        False: "no",
        None: "empty",
        }
## For the function take() inside Parser.parse()
OPEN = {"such", "so"}
CLOSE = {"wow", "many"}

WORDCHARS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890."
DIGITS = set("1234567")
NOPRINT = set(chr(c) for c in range(0x20))

def typeOf(obj):
    return type(obj).__name__

def severalThings(iterable):
    items = list(iterable)
    text = ""
    for obj in items[:-1]:
        text += repr(obj) + ", "
    return text + "or " + repr(items[-1])

class Parser(object):
    def __init__(self, text, separators={" ", "\n", "\r", "\v", "\t"}, wordchars=WORDCHARS, list_separators={"and", "also"}, declarators={"is", ",", ".", "!", "?"}):
        self.text = text
        self.separators = set(copy(separators))
        self.wordchars = set(wordchars).union(declarators)
        self.list_separators = set(copy(list_separators))
        self.declarators = set(copy(declarators))

    def tokenize(self):
        tokens = []
        chars = iter(self.text)
        line = 1
        column = 1
        for char in chars:
            ## String
            if char == "\n":
                line += 1
                column = 0
            column += 1

            if char in ("\"", "'"):
                terminator = char
                strval = ""
                for char in chars:
                    if char in NOPRINT:
                        raise SyntaxError("On {} / {}, illegal character in string".format(line, column))
                    if char == "\\":
                        strval += char + next(chars)
                    elif char == terminator:
                        break
                    else:
                        strval += char
                    column += 1
                tokens.append((strval, "str", (line, column - len(strval))))

            ## Start of word
            elif char not in self.separators and char in self.wordchars:
                wordval = char
                for char in chars:
                    if char == "\n":
                        line += 1
                        column = 0
                    if char in self.separators or char not in self.wordchars:
                        break
                    column += 1
                    wordval += char
                if wordval in constants:
                    tokens.append((wordval, "constant", (line, column - len(wordval))))
                else:
                    tokens.append((wordval, "word", (line, column - len(wordval))))

            elif char in self.separators:
                pass

            else:
                raise SyntaxError("On {} / {}".format(line, column))

        return tokens

    def parse(self, tokens_list):
        def take(tokens, close_words=CLOSE, open_words=OPEN):
            level = 1
            for token in tokens:
                if token[0] in close_words:
                    level -= 1
                elif token[0] in open_words:
                    level += 1
                yield token
                if level == 0:
                    break

        ## First token
        token, tokentype, location = tokens_list[0]
        tokens = iter(tokens_list)

        ## Check for comment
        if token == "silent":
            take(tokens, close_words=["loud"], open_words=[])

        ## Possibly single atom value
        if (len(tokens_list) == 1) or (len(tokens_list) == 2 and tokens_list[-1][0] in CLOSE):
            if tokentype == "str":
                return self.parseString(token, location)
            elif tokentype == "constant" and token in constants:
                return constants[token]
            elif tokentype == "word" and token == "many":
                ## Empty list
                return []
            else:
                return self.parseNumber(token, location)

        value = None
        for token, tokentype, location in tokens:
            if token == "such":
                if value == None:
                    value = {}
                ## Expecting string value here
                token, tokentype, location = next(tokens)
                if tokentype != "str":
                    raise SyntaxError("On {} / {} expected string value here".format(location[0], location[1]))
                try:
                    if next(tokens)[0] not in self.declarators:
                        raise SyntaxError("On {} / {} expected {}".format(location[0], location[1], severalThings(self.declarators)))
                except StopIteration:
                    raise SyntaxError("On {} / {} expected {} got EOF".format(location[0], location[1], severalThings(self.declarators)))
                value[token] = self.parse(list(take(tokens)))

            if token == "so":
                if value == None:
                    value = []
                for token, tokentype, location in tokens:
                    if token == "many":
                        ## End of list
                        break
                    elif token == "so":
                        ## Nested list
                        ts = list(take(tokens))
                        value.append(self.parse([(token, tokentype, location)] + ts))
                        continue
                    elif token == "such":
                        ts = list(take(tokens, open_words=[], close_words=["also", "and"]))
                        value.append(self.parse([(token, tokentype, location)] + ts))
                        continue
                    else:
                        ## Atom value
                        value.append(self.parse([(token, tokentype, location)]))

                    ## Separator between values in list
                    separator, _, location = next(tokens)
                    if separator == "many":
                        break
                    if separator not in self.list_separators:
                        raise SyntaxError("On {} / {} expected {} got {}".format(location[0], location[1], severalThings(self.list_separators), repr(separator)))

        return value

    def parseString(self, string, location):
        def getEscape(chars):
            for char in chars:
                if char == "b": return "\b"
                elif char == "f": return "\f"
                elif char == "n": return "\n"
                elif char == "r": return "\r"
                elif char == "t": return "\t"
                elif char == "'": return "'"
                elif char == "\"": return "\""
                elif char == "u":
                    try:
                        digits = "".join([next(chars) for _ in range(6)])
                    except StopIteration:
                        raise SyntaxError("On {} / {} expected six digits".format(location[0], location[1]))
                    if not all(digit in DIGITS for digit in digits):
                        raise SyntaxError("On {} / {} expected octal digits".format(location[0], location[1]))
                    return chr(int(digits, 8))
            return "\\"
        chars = iter(string)
        value = ""
        for char in chars:
            if char == "\\":
                escaped = getEscape(chars)
                value += escaped
            else:
                value += char
        return value

    def parseNumber(self, string, location):
        hasvery = string.count("very")
        if hasvery > 1:
            raise SyntaxError("On {} / {} Invalid number {}".format(location[0], location[1], string))
        if hasvery == 1:
            string = string.replace("very", "e")

        hasfraction = string.count(".")
        if hasfraction > 1:
            raise SyntaxError("On {} / {} Invalid number {}".format(location[0], location[1], string))
        if hasfraction == 1 or hasvery == 1:
            try:
                return float(string)
            except:
                pass

        try:
            return int(string)
        except:
            print(string)
            raise SyntaxError("On {} / {} Invalid number".format(location[0], location[1]))

class Serializer(object):
    def __init__(self, obj, indent=2, eol="\n"):
        self.obj = obj
        self.eol = eol
        self.indent = indent

    def serialize(self):
        self.text = ""
        def rec(obj, level, newline):
            if type(obj).__name__ in ["str", "int"]:
                if newline:
                    self.text += (self.indent * level) * " "
                self.text += repr(obj) + " "

            ## Python 2 stuff
            elif type(obj).__name__ == "unicode":
                if newline:
                    self.text += (self.indent * level) * " "
                self.text += repr(obj)[1:] + " " ## Remove the 'u' upfront

            elif obj in tuple(constants_reverse):
                if newline:
                    self.text += (self.indent * level) * " "
                self.text += constants_reverse[obj]
            elif type(obj).__name__ == "list":
                if newline:
                    self.text += (self.indent * level) * " "
                self.text += "so" + self.eol
                if obj:
                    self.text += (self.indent * (level+1))*" "
                    for i in range(len(obj)):
                        sub = obj[i]
                        if typeOf(sub) == "dict":
                            self.text += self.eol
                            rec(sub, level + 1, True)
                        else:
                            rec(sub, level + 1, False)
                        if i+1 < len(obj):
                            self.text += "and "
                    if typeOf(obj[-1]) in ["list", "dict"]:
                        self.text += "many" + self.eol
                    else:
                        self.text += self.eol + (self.indent * level)*" " + "many" + self.eol
                else:
                    self.text += "many"
            elif typeOf(obj) == "dict":
                for key in obj:
                    if newline:
                        self.text += (self.indent * level) * " "
                    self.text += "such {} is{}".format(repr(str(key)), self.eol)
                    rec(obj[key], level + 1, True)

                    if type(obj[key]).__name__ == "dict":
                        self.text += "wow" + self.eol
                    elif type(obj[key]).__name__ == "list":
                        self.text += (self.indent * level) * " " + "wow" + self.eol
                    else:
                        self.text += self.eol + (self.indent * level) * " " + "wow" + self.eol
            else:
                raise TypeError("Cannot serialize {}".format(type(obj).__name__))
        rec(self.obj, 0, True)
        return self.text

## XXX: Unlike json.dump and json.load, Dson.load and Dson.dump take a path as their first
##      argument
def loads(string):
    parser = Parser(string)
    tokens = parser.tokenize()
    return parser.parse(tokens)

def load(path):
    with open(path, "rb") as r:
        return loads(r.read())

def dumps(obj, indent=0):
    serializer = Serializer(obj, indent=indent)
    return serializer.serialize()

def dump(obj, path, indent=0):
    with open(path, "wb") as w:
        return w.write(dumps(obj, indent=indent))
