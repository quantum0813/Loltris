#!/usr/bin/python2

import Jobs
import Log
import functools as Func

def textBoxes(pairs, game, **kwargs):
    return [Jobs.AutoTextBox(game, text, onmouseclick=func, **kwargs) for text, func in pairs]

def switches(pairs, game, **kwargs):
    return [
            Jobs.Switch(
                game,
                text,
                funcs[0],
                funcs[1],
                **kwargs
                )
            for text, funcs in pairs
            ]

def basicSwitches(pairs, game, turnOn, turnOff, lookup, **kwargs):
    switches = []
    for text, option in pairs:
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