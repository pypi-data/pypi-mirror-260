# hist_events.py
# Deifnitions of history events, for appending to files' history.


import time
from treerec.trace_ancestors import *
from treerec.pathtuputils import subtract_paths


def record_entry(dictin:dict, session:str=None, localpath:str=None):
    event = {
        'type': 'record',
        'name': dictin['name'],
        'device': dictin['device'],
        'hash': dictin['hash']
        }
    if localpath:
        event['localpath'] = localpath
    return {
        'time' : int(time.time()),
        'session' : session,
        'name' : dictin['name'],
        'event' : event
    }


def move_entry(source, destination, session=None):
    # remember to fix broken ties, or leave a log for the inactive trees to fix it
    pass


def check_tied(source:dict, destination:dict):
    # Check the ties of two entries to see if they are tied.
    # Returns True if *both files* have ties pointing to each other,
    #   and False otherwise.
    D_uuid = get_tree_id(destination)
    S_uuid = get_tree_id(source)
    S_in_D = False
    D_in_S = False
    for tie_entry in destination['ties']:
        if tie_entry['uuid']==S_uuid and tie_entry['path']==source['path']:
            S_in_D = True
            break
    for tie_entry in source['ties']:
        if tie_entry['uuid']==D_uuid and tie_entry['path']==destination['path']:
            D_in_S = True
            break
    if S_in_D and D_in_S:
        return True
    else:
        return False


def compare_hashes(dictA:dict, dictB:dict):
    """
    Return True if the hashes are identical, and not a fail value
    (e.g. hash == 0, -1).
    """
    if type(dictA.get('hash', 0)) is str and type(dictB.get('hash', 0)) is str:
        return dictA['hash']==dictB['hash']
    return False


def tie_entry(source:dict, destination:dict, session:str=None):
    # First, check to see if the files are already tied
    if check_tied(source, destination):
        return False
    # Else, return the tie event
    root = find_current_root(destination)
    after_root_path = subtract_paths(root['path'], destination['path'])
    root_nickname = root.get('nickname', root['name'])
    nickname_path = (root_nickname, *after_root_path)
    return {
        'time' : int(time.time()),
        'session' : session,
        'name' : source['name'],
        'event' : {
            'type' : 'tie',
            'source' : source['path'],
            'name' : destination['name'],
            'device' : destination['device'],
            'uuid' : get_tree_id(destination),
            'session' : (session if session else destination.get('session', None)),
            'time': int(time.time()),
            'path' : destination['path'],
            'nickname_path': nickname_path,
            'hash': destination.get('hash', 0),
            'identical_hash': compare_hashes(source, destination)
        }
    }


def update_entry(dictin:dict, update_info:dict, session:str=None):
    update_fields = [attr for attr in update_info]
    return {
        'time' : int(time.time()),
        'session' : session,
        'name' : dictin['name'],
        'event' : {
            'type' : 'update',
            'old' : {key: dictin[key] for key in update_fields},
            'new' : {key: update_info[key] for key in update_fields}
            }
        }
