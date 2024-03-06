# entryutils.py
# Utilities for entry-level operations
# Includes: tying files, updating files, printing file info.


from treerec.primitives import *
from treerec.hist_events import *
from treerec.dictutils import *
from treerec.dirutils import *
from treerec.pathtuputils import *
from treerec.navutils import *
import time, datetime


def std_print(entry:dict, field:str, failstr:str=FIELD_NOT_RECORDED):
    # The point of this is that it prints 'N/A' if *either* the field
    # is not present, or if it's present with a value of None or False.
    return (entry[field] if entry.get(field, False) else failstr)


def time_formatted(itime):
    if itime==-1:
        return ''
    return datetime.datetime.fromtimestamp(int(itime)).strftime(DATE_FORMAT + '  ' + TIME_FORMAT)


def std_time(entry, time_key:str, failstr:str=FIELD_NOT_RECORDED):
    return (time_formatted(entry[time_key]) if entry.get(time_key, False)
            else failstr)

def std_hash(entry:dict, failstr:str=FIELD_NOT_RECORDED, abbrev:bool=False):
    hash_data = entry.get('hash', False)
    if hash_data==-1:
        return NO_HASH_BC_DIR
    elif hash_data==-2:
        return NO_HASH_BC_PERMISSIONS
    elif not hash_data:
        return failstr
    elif abbrev:
        if len(hash_data)>=7:
            return hash_data[0:7]
        else:
            return hash_data
    else:
        return hash_data


def std_hist_session(entry, idx:int, failstr:str=FIELD_NOT_RECORDED):
    try:
        session = (entry['history'][idx]['session'] if entry['history'][idx].get('session', False)
                else failstr)
        mtime = (entry['history'][idx]['time'] if entry['history'][idx].get('time', False) else '')
        return '"' + session + '" @ ' + time_formatted(mtime)
    except:
        return failstr


def print_dict_info(
        entry,
        data=('owner', 'device',
              'nicknamepath', 'treepath', 'os_type', 'ctime', 'mtime', 'atime','hash',
              'notes', 'ties', 'history', 'recordedsession', 'lastmodifiedsession')):
    print("  Name: " + entry['name'])
    print("  Type: " + entry['type'])
    if entry['type'] == 'unrecorded':
        return
    SP = SuperPath(entry)
    printouts = {
        'owner': "  Owner: " + std_print(entry, 'owner'),
        'device': "  Device: " + std_print(entry, 'device'),
        'nicknamepath': "- Path: (" + SP.root_nickname + ")/" + SP.print_after_root(),
        'treepath': "- Tree Path: " + SP.print_path(),
        'os_type': "- OS Type: " + std_print(entry, 'os_type'),
        'ctime': "- C-time: " + std_time(entry, 'ctime'),
        'mtime': "- Modified: " + std_time(entry, 'mtime'),
        'atime': "- Accessed: " + std_time(entry, 'atime'),
        'hash': '- Hash: ' + std_hash(entry),
        'abbrev-hash': '- Hash: ' + std_hash(entry, abbrev=True),
        'notes': "> Notes: " + str(len(entry.get('notes', []))),
        'ties': "> Ties: " + str(len(entry.get('ties', []))),
        'history': "> History: " + str(len(entry.get('history', []))),
        'recordedsession': '> Recorded: Session ' + std_hist_session(entry, 0),
        'lastmodifiedsession': '> Last modified: Session ' + std_hist_session(entry, -1)
    }
    for key in data:
        print(printouts[key])

def print_os_file_info(filename,
                       do_hash=True,
                       data=('name', 'owner', 'type', 'path', 'os_type',
                             'ctime', 'mtime', 'atime', 'hash')):
    pathlike = full_Path(filename)
    if not pathlike:
        return
    if not pathlike.exists():
        print('Error locating file ' + str(pathlike))
        return
    stat = pathlike.stat()
    owner = fileobj_get_owner(pathlike)
    hash_data = (hash_file(pathlike) if do_hash else 0)
    if hash_data==-1:
        hash_print = NO_HASH_BC_DIR
    elif hash_data==0:
        hash_print = FIELD_NOT_RECORDED
    else:
        hash_print = hash_data
    printouts = {
        'name': '  Name: ' + pathlike.name,
        'owner': '  Owner: ' + (str(owner) if owner else FIELD_NOT_RECORDED),
        'type': '  Type: ' + ('dir' if valid_dir(pathlike, verbose=False) else 'file'),
        'path': '  Path: ' + str(pathlike),
        'os_type': '  OS Type: ' + os.name,
        'ctime': '- C-time: ' + time_formatted(stat.st_ctime),
        'mtime': '- Modified: ' + time_formatted(stat.st_mtime),
        'atime': '- Accessed: ' + time_formatted(stat.st_atime),
        'hash': '- Hash: ' + hash_print 
    }
    for key in data:
        print(printouts[key])


def new_entry_in_dir(parent_dict, objname, device=None, os_type=None, session=None, quiet=False, do_hash=True):
    """
    Records a new entry in the given directory.
    Converts treepath into localpath, pulls system information, then records treepath to new entry.
    """
    parent_localpath = combine_pathtuples(get_localpath_from_path(parent_dict))
    obj_pathlike = full_Path(Path(parent_localpath) / objname)
    if not obj_pathlike:
        return False
    new_dict = create_dict(obj_pathlike, 
                           rootname=parent_dict.get('root'), 
                           session=session, 
                           device=device, 
                           os_type=os_type,
                           do_hash=do_hash)
    if new_dict==False:
        return False
    newdict_treepath = (*parent_dict['path'], objname)
    new_dict['path'] = newdict_treepath
    return replace_entry_in_dir(parent_dict, new_dict, quiet=quiet)


def update_unrecorded_contents(dictin:dict, pathlike:Path=None, quiet:bool=False):
    """
    Updates the contents of a directory dict with the contents of the directory at pathlike.
    Adds new unrecorded files, and removes unrecorded files present in tree but not in pathlike.
    """
    if not pathlike:
        pathlike = Path(combine_pathtuples(calculate_localpath(dictin)))
    if dictin['type']==DEVINFO:
        # DEVINFO has children which are not in a tree structure mirrored
        # by the tree structure on the system
        # I.e., the roots are in locations all over the place.
        return False
    if dictin['type'] not in DIR_LIST_TYPES:
        if not quiet: print("Cannot update contents of non-directory.")
        return False
    try:
        stat = pathlike.stat()
    except FileNotFoundError:
        if not quiet: print("File not found at path " + str(pathlike))
        return False
    except PermissionError:
        print('Permission denied.')
        return False
    except:
        print('Unable to update unrecorded contents.')
        return False
    contents_list = [pathlike/entry
            for entry in os.listdir(pathlike)]
    dict_dir_names = [entry['name'] 
            for entry in dictin['dir_list']]
    dict_file_names = [entry['name'] 
            for entry in dictin['file_list']]
    sys_dir_names = [entry.name
            for entry in contents_list 
            if valid_dir(entry, verbose=True)]
    sys_file_names = [entry.name 
            for entry in contents_list 
            if not valid_dir(entry, verbose=False)]
    # check for missing dirs in dict
    for entry in sys_dir_names:
        if entry not in dict_dir_names:
            dictin['dir_list'].append( {
                    'name': entry, 
                    'type': 'unrecorded'
                    } )
    # check for missing dirs in sys
    for idx in reversed(range(len(dictin['dir_list']))):
        entry = dictin['dir_list'][idx]
        if entry['type']=='unrecorded' and entry['name'] not in sys_dir_names:
            dictin['dir_list'].pop(idx)
    # check for missing files in dict
    for entry in sys_file_names:
        if entry not in dict_file_names:
            dictin['file_list'].append( {
                'name': entry,
                'type': 'unrecorded'
                } )
    # check for missing files in sys
    for idx in reversed(range(len(dictin['file_list']))):
        entry = dictin['file_list'][idx]
        if entry['type']=='unrecorded' and entry['name'] not in sys_file_names:
            dictin['file_list'].pop(idx)
    # alphebatize the results:
    dictin['dir_list'] = sorted(dictin['dir_list'], key=lambda x: str.casefold(x['name']))
    dictin['file_list'] = sorted(dictin['file_list'], key=lambda x: str.casefold(x['name']))
    """
    for entry in contents_list:
        if entry.is_dir():
            if entry.name not in dict_dir_names:
                dictin['dir_list'].append({'name': entry.name, 'type': 'unrecorded'})
        elif entry.name not in dict_file_names:
            dictin['file_list'].append({'name': entry.name, 'type': 'unrecorded'})
    # if we find an unrecorded entry in dictin which is not in contents_list, remove it:
    for x_list in ['dir_list', 'file_list']:
        for idx in reversed(range(len(dictin[x_list]))):
            entry = dictin[x_list][idx]
            if entry['type']=='unrecorded' and (entry['name'] not in [x.name for x in contents_list]):
                dictin[x_list].pop(idx)
    """
    return dictin

def update_object(dictin:dict, pathlike:Path=None, session:str=None, do_hash:bool=True, quiet:bool=False):
    if dictin['type']=='unrecorded':
        return False, False
    if dictin['type']==DEVINFO:
        # DEVINFO is not a directory on the system.
        if not quiet: print('Cannot update DEVINFO: it is not a system directory.')
        return False, False
    if not pathlike:
        pathlike = Path(combine_pathtuples(calculate_localpath(dictin)))
    try:
        stat = pathlike.stat()
    except FileNotFoundError:
        if not quiet: print("File not found at path " + str(pathlike))
        return False, False
    update_info = {
        'name' : dictin['name'],
        'owner' : fileobj_get_owner(pathlike),
        'ctime' : int(stat.st_ctime),
        'mtime' : int(stat.st_mtime),
        'atime' : int(stat.st_atime),
        'hash' : (hash_file(pathlike) if do_hash else 0)
    }
    identical = True
    for attr in update_info:
        if dictin.get(attr, None) != update_info[attr]:
            identical = False
            break
    if identical:
        if not quiet: print('%%% is identical.')
        return dictin, False
    dictin['history'].append(update_entry(dictin, update_info, session=session))
    for attr in update_info:
        dictin[attr] = update_info[attr]
    if dictin['type'] in DIR_LIST_TYPES:
        dictin = update_unrecorded_contents(dictin, pathlike, quiet)
    return dictin, True


def tie_files(dict1, dict2, session=None, quiet:bool=False):
    if dict1['type']=='unrecorded':
        print("Cannot tie unrecorded file: " + dict1['name'])
        return False
    if dict2['type']=='unrecorded':
        print("Cannot tie unrecorded file: " + dict2['name'])
        return False

    dict1_event = tie_entry(dict1, dict2, session=session)
    if not dict1_event:
        print('Files are already tied.')
        return False
    dict2_event = tie_entry(dict2, dict1, session=session)
    dict1_tie = dict1_event['event']
    dict2_tie = dict2_event['event']
    if not quiet:
        print('.. ' 
                + dict2_tie['nickname_path'][0] + '> | '
                + dict2_tie['name'] + ' -> '
                + dict1_tie['nickname_path'][0] + '> | '
                + dict1_tie['name']
                )

    dict1['ties'].append(dict1_tie)
    dict2['ties'].append(dict2_tie)
    dict1['history'].append(dict1_event)
    dict2['history'].append(dict2_event)

    return True


def print_update_event_file_data(sub_event:dict, diff_list:list=None):
    def indent(key):
        if diff_list:
            charout = '   ' + ('*' if key in diff_list else ' ')
        else:
            charout = '    '
        return charout

    return (
            indent('owner') + "Owner: " + std_print(sub_event, 'owner') + '\n' +
            indent('ctime') + "C-time: " + std_time(sub_event, 'ctime') + '\n' +
            indent('mtime') + "Modified: " + std_time(sub_event,'mtime') + '\n' +
            indent('atime') + "Accessed: " + std_time(sub_event,'atime') + '\n' +
            indent('hash') + "Hash: " + std_hash(sub_event) + '\n'
        )


def print_update_event_data_with_diff(event:dict):
    """
    Prints all of the fields for an update event,
    with an '*' next to those fields which changed.
    """
    diff_list = [key for key in event['old'] if event['old'][key]!=event['new'].get(key,None)]
    return (
        '--Old: ' + '\n' + print_update_event_file_data(event['old'], diff_list=None) +
        '--New: ' + '\n' + print_update_event_file_data(event['new'], diff_list) + '\n')


def print_history_event(dictin:dict, idx:int):
    if idx>=len(dictin['history']):
        return False
    histevent = dictin['history'][idx]
    event = histevent['event']
    header = (">> " + std_time(histevent, 'time') + ', ' +
              'Session: ' + std_print(histevent, 'session') + '\n')
    if event['type']=='record':
        return header + ('Recorded ' + std_print(event, 'name') + '\n' +
                         'Device: ' + std_print(event, 'device') + '\n' +
                         'Local path: ' + std_print(event, 'localpath') + '\n' +
                         'Hash: ' + std_hash(event) + '\n')
    elif event['type']=='tie':
        return header + ('Tied \n' +
                         std_print(dictin, 'device') + ': ' + combine_pathtuples(event['source']) + '\n' +
                         'to \n' +
                         std_print(event, 'device') + ': ' + combine_pathtuples(event['path']) + '\n')
    elif event['type']=='update':
        return header + ('Updated ' + std_print(histevent, 'name') + '\n' + 
                         print_update_event_data_with_diff(event))


def print_dict_history_full(dictin:dict):
    for idx, _ in enumerate(dictin['history']):
        print(print_history_event(dictin, idx))
