from copy import copy

# Helper functions for creating action_func functions and initial parameter dictionaries.

def mykey_func(key, value):
    """Returns a function that sets the key of a dict to
    the value given in this file."""
    def setkey(dictin, cval):
        dictin[key] = value
        return copy(dictin)
    return setkey

def set_command(commandname):
    def setkey(dictin, cval):
        dictin['command'] = commandname
        return copy(dictin)
    return setkey

def theirkey_func(key):
    """
    Returns a function that sets the key of a dict to
    the value entered on the command line.
    """
    def setkey(dictin, cval):
        dictin[key] = cval
        return copy(dictin)
    return setkey

def blank_func():
    """
    Returns a function that passes the dict through unchanged.
    """
    def passfunc(dictin, cval):
        return dictin
    return passfunc

def blank_dict(command, *args):
    return {'command': command} | {arg: None for arg in args}