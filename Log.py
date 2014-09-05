#!/usr/bin/python2 
#-*- coding: utf-8 -*-

## =====================================================================
## Tools for logging
## Copyright (C) 2014 Jonas Møller <jonasmo441@gmail.com>
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

import inspect, sys, traceback as Traceback
from time import time, ctime, strftime, localtime
from sys import stdout
from threading import currentThread
from pprint import pprint

from Globals import *

enable_color = False
color = {
        "DEFAULT": "\x1b[0;00m",
        "PANIC": "\x1b[1;31m",
        "FAIL": "\x1b[1;31m",
        "NOTICE": "",
        "DEBUG": "",
        "TMPDEBUG": "",
        "ERROR": "\x1b[1;33m",
        "WARNING": "\x1b[1;31m",
        }

loglevel = {
        "FAIL": 0,
        "PANIC": 0,
        "ERROR": 1,
        "WARNING": 2,
        "NOTICE": 3,
        "DEBUG": 4,
        "TMPDEBUG": 5,
        }

def out(msg, end="\r\n", c="\x1b[0;33m"):
    stdout.write((c if c else "") + str(msg) + ("\x1b[0;00m" if c else "") + str(end))
    stdout.flush()

def fprint(fileobj, data):
    fileobj.write(data + EOL)
    fileobj.flush()

## Safe print
def putLn(thing):
    try:
        print(thing)
    except:
        pass

def put(thing):
    try:
        stdout.write(str(thing))
    except:
        pass

def genericLog(logtype, message, cr=False, **kwargs):
    if loglevel[logtype] > LOGLEVEL:
        return

    if cr:
        ## Carriage return
        put("\r")
    if enable_color:
        put(color.get(logtype, ""))
    log = "[%s] %8s: %20s: %s" % (getTime(), logtype, getCaller(), message)
    putLn(log)
    if enable_color:
        put(color["DEFAULT"])
    if kwargs.get("trace"):
        ## Print the traceback, indented with four spaces
        put("".join(["    "+x+EOL for x in Traceback.format_exc(kwargs["trace"]).splitlines()]))

## Just so that everything is uniform
def dump(obj):
    if loglevel["DEBUG"] > LOGLEVEL:
        ## All dumping is considered to be debugging
        return
    put(str(obj))

def stackDump():
    if loglevel["DEBUG"] > LOGLEVEL:
        return
    Traceback.print_stack()

## Called by genericLog, which is called by panic/error/log etc, which is called by [function we want]
def getCaller():
    curframe = inspect.currentframe()
    return inspect.getouterframes(curframe, 2)[3][3]

def getTime(spec="%H:%M:%S"):
    return strftime(spec, localtime(time()))

def panic(comment, **kwargs):
    genericLog("PANIC", comment, **kwargs)
    if kwargs.get("exception"):
        raise kwargs["exception"]
    fail(255)

def fail(ret, **kwargs):
    genericLog("FAIL", "Failing due to previous errors... Ignucius help us", **kwargs)
    sys.exit(ret)

def notice(comment, **kwargs):
    genericLog("NOTICE", comment, **kwargs)

def debug(comment, **kwargs):
    genericLog("DEBUG", comment, **kwargs)

def error(comment, **kwargs):
    genericLog("ERROR", comment, **kwargs)

def log(comment, **kwargs):
    genericLog("NOTICE", comment, **kwargs)

def warning(comment, **kwargs):
    genericLog("WARNING", comment, **kwargs)

def tempDebug(comment, **kwargs):
    genericLog("TMPDEBUG", comment, **kwargs)
