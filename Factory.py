#!/usr/bin/python2

import Jobs
import Log
import functools as Func

def textBoxes(dubs, game, **kwargs):
    boxes = []
    for text, func in dubs:
        Log.debug("Generating textbox {}".format(repr(text)))
        boxes.append(Jobs.AutoTextBox(game, text, onmouseclick=func, **kwargs))
    return boxes
    ## XXX: Needed debug
    # return [Jobs.AutoTextBox(game, text, onmouseclick=func, **kwargs) for text, func in dubs]

def switches(dubs, game, **kwargs):
    return [
            Jobs.Switch(
                game,
                text,
                funcs[0],
                funcs[1],
                **kwargs
                )
            for text, funcs in dubs
            ]

def basicSwitches(dubs, game, turnOn, turnOff, lookup, **kwargs):
    switches = []
    for text, option in dubs:
        switches.append(
                Jobs.Switch(
                    game,
                    text,
                    Func.partial(turnOn, option, lookup),
                    Func.partial(turnOff, option, lookup),
                    ison=lookup.get(option, False),
                    **kwargs
                    )
                )
    return switches

def variableTextBoxes(trips, game, **kwargs):
    boxes = []
    for text, variables, func in trips:
        boxes.append(Jobs.AutoTextBox(game, text, variables=variables, onmouseclick=func, **kwargs))
    return boxes

def sliders(dubs, game, **kwargs):
    pass
