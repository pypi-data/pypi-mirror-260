from pathlib import Path
import os, time
from treerec.primitives import *
from treerec.hist_events import record_entry
import hashlib
import uuid



def hash_file(pathlike):
    """
    Given a Path object, return the sha256 hash of its contents.
    By convention, a hash of -1 indicates that the file is a directory,
      a hash of -2 indicates a lack of permission to hash the file,
      and a hash of 0 indicates that the hash was not taken on a file.
    """
    if valid_dir(pathlike, verbose=True):
        return -1
    try:
        with open(pathlike, 'rb') as f:
            return hashlib.sha256(f.read()).hexdigest()
    except PermissionError:
        return -2
    except:
        return 0


def fileobj_get_owner(pathlike):
    if os.name=='nt':
        from treerec import winutils
        return winutils.get_win_info(pathlike)[0]
    elif os.name=='posix':
        return pathlike.owner()


def valid_dir(pathlike:Path, verbose:bool=False):
    Out = False
    try:
        Out = pathlike.is_dir()
    except OSError:
        if verbose: print('System cannot access "' + pathlike.name + '".')
    return Out


def fileobj_alphabetize(dictin:dict):
    if dictin.get('dir_list', False):
        dictin['dir_list'] = sorted(dictin['dir_list'], key=lambda x: str.casefold(x['name']))
    if dictin.get('file_list', False):
        dictin['file_list'] = sorted(dictin['file_list'], key=lambda x: str.casefold(x['name']))
       

def create_dict(pathlike, rootname=None, device=None, os_type=None, session=None, objtype='auto', nickname=None, do_hash=True, include_uuid=False):
    try:
        stat = pathlike.stat()
    except FileNotFoundError:
        print("File not found at path " + str(pathlike))
        return False
    except OSError:
        print("System cannot access file at path " + str(pathlike))
        return False
    objtype = (('dir' if valid_dir(pathlike) else 'file') if objtype=='auto' else objtype)
    hash_data = (hash_file(pathlike) if do_hash else 0)
    out = {
        'name' : pathlike.name,
        'root' : rootname,
        'path' : pathlike.parts,
        'type' : objtype,
        'owner' : fileobj_get_owner(pathlike),
        'device' : device,
        'os_type' : (os_type if os_type else os.name),
        'ctime' : int(stat.st_ctime),
        'mtime' : int(stat.st_mtime),
        'atime' : int(stat.st_atime),
        'hash' : hash_data,
        'notes' : [],
        'ties' : [],
        'history' : []
    }
    out['history'].append(record_entry(out, session=session, localpath=str(pathlike)))
    if include_uuid:
        out['uuid'] = uuid.uuid4().hex
    if objtype in DIR_LIST_TYPES:
        contents_list = [pathlike/entry for entry in os.listdir(pathlike)]
        out['dir_list'] = [{'name' : entry.name, 'type' : 'unrecorded'} for entry in contents_list if valid_dir(Path(entry), verbose=True)]
        out['file_list'] = [{'name' : entry.name, 'type' : 'unrecorded'} for entry in contents_list if not valid_dir(Path(entry), verbose=False)]
        fileobj_alphabetize(out) # I think the sorting is unnecessary, but I'll do it anyway for good measure
    if nickname:
        out['nickname'] = nickname
    return out


def create_dict_pure(
        objname:str=None, 
        objtype:str=None,
        objpath:str=None,
        owner:str=None,
        device:str=None,
        os_type:str=None,
        ctime:int=None,
        mtime:int=None,
        atime:int=None,
        shortcut_destination=None,
        nickname:str=None,
        include_uuid:bool=False):
    out = {
        'name' : objname,
        'path' : objpath,
        'type' : objtype,
        'owner' : owner,
        'device' : device,
        'os_type' : os_type,
        'ctime': ctime,
        'mtime' : mtime,
        'atime' : atime,
        'hash' : 0,
        'notes' : [],
        'ties' : [],
        'history' : []
    }
    if include_uuid:
        out['uuid'] = uuid.uuid4().hex
    if objtype in DIR_LIST_TYPES:
        out['dir_list'] = []
        out['file_list'] = []
    if objtype=='shortcut':
        out['shortcut_destination'] = shortcut_destination
    if nickname!=None:
        out['nickname'] = nickname
    return out


def get_position_in_parent(dictin:dict, nickname_first:bool=False):
    """
    Returns the index and list of dictin in its parent dict.
    """
    parent = dictin.get(PARENT, False)
    if not parent:
        print("Error finding parent dictionary.")
        return False, False
    if nickname_first:
        name_priority = ['nickname', 'name']
    else:
        name_priority = ['name', 'nickname']
    for nametype in name_priority:
        for x_list in ['dir_list', 'file_list']:
            for idx, entry in enumerate(parent[x_list]):
                if entry.get(nametype) and entry.get(nametype)==dictin.get(nametype):
                    return idx, x_list
    print("Entry name not found in parent dictionary.")
    return False, False


def find_current_root(dirdict):
    if dirdict['type'] == DEVINFO:
        return dirdict
    curdir = dirdict
    parentdir = dirdict[('parent',)]
    while parentdir['type'] != DEVINFO:
        curdir = parentdir
        parentdir = curdir[('parent',)]
    return curdir


def get_tree_id(dirdict):
    """
    Given a directory dict, return the ID of the tree it is in.
    """
    root = find_current_root(dirdict)
    return root[('parent',)]['uuid']


def get_recorded_session_name(dictin):
    for event in dictin['history']:
        if event['event']['type']=='record':
            return event['session']


def print_basic_info(dictin):

    def print_thing(label, key, default=FIELD_NOT_RECORDED):
        dictin_get = dictin.get(key, None)
        print(label + ': ' + (str(dictin_get) if (dictin_get is not None) else default))

    print("Name: " + dictin['name'])
    print("Type: " + dictin['type'])
    if dictin.get('type', 'unrecorded')=='unrecorded':
        return
    first_modified_session = get_recorded_session_name(dictin)
    last_modified_session = dictin['history'][-1]['session']
    print_thing('Path', 'path')
    if dictin.get('localpath', None):
        print_thing('Local Path', 'localpath')
    print_thing('Owner', 'owner')
    print_thing('Device', 'device')
    print_thing('OS type', 'os_type')
    print('Recorded during: Session "', first_modified_session,'".')
    print('Last modified during: Session "', last_modified_session,'".')
    print_thing('Creation time', 'ctime')
    print_thing('Modification time', 'mtime')
    print_thing('Access time', 'atime')
    print_thing('Notes', 'notes', default='None')
    print_thing('Ties', 'ties', default='None')
    print_thing('History', 'history', default='None')


def print_dict_history(dictin):
    if dictin.get('type', 'unrecorded')=='unrecorded':
        print('Cannot print history of an unrecorded entry')
        return False
    for entry in dictin.get('history', None):
        event_type = entry['event']['type']
        print('>> ' + event_type + " // " + time.ctime(entry['time']))
        print('   Session: ' + entry.get('session', 'None'))
        if event_type=='tie':
            print('   -------------')
            print('   Name: ' + entry['event']['name'])
            print('   Device: ' + entry['event']['device'])
        print('  ')


def dict_add_note(dictin, note_text='', session=None):
    if dictin.get('type', 'unrecorded')=='unrecorded':
       print('Cannot add note to an unrecorded entry.')
       return False
    if note_text=='':
        return False
    dictin['notes'].append({
        'time' : time.time(),
        'session' : session,
        'text' : note_text
    })
    return True


def print_dict_notes(dictin):
    if dictin.get('type', 'unrecorded')=='unrecorded':
        print(' [no notes - unrecorded file]')
        return
    if len(dictin.get('notes', []))==0:
        print(' [no notes]')
        return
    for idx, entry in enumerate(dictin.get('notes', [])):
        print('>> Note ' + str(idx) + ' // ' + time.ctime(entry['time']))
        print('   Session: ' + entry.get('session', 'None'))
        print(entry['text'])
        print('-------------------------')
