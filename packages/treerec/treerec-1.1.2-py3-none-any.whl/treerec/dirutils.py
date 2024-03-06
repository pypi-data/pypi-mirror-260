from treerec.primitives import *
from treerec.pathtuputils import *
from treerec.dictutils import *


def full_Path(pathstr:str, verbose:bool=True):
    """
    Takes a string or Path object and returns full Path object.
    Handles errors and returns False if any error occurred.
    """
    try:
        pathlike = Path(pathstr).resolve().absolute()
        return pathlike
    except OSError:
        if verbose: print('System cannot access "' + str(pathstr) + '".')
        return False
    except Exception as error:
        print(error)
        return False


def calculate_localpath(dictin:dict):
    if dictin['type']=='unrecorded':
        return False
    if dictin.get('nickname', False):
        return dictin['localpath']
    elif len(dictin['path'])==0:
        print("Error: no path for object " + dictin['name'])
        return False
    pathparts = [dictin['name']]
    cdir = dictin
    while not cdir[PARENT].get('nickname', False):
        cdir = cdir[PARENT]
        pathparts = [cdir['name']] + pathparts
    cdir = cdir[PARENT]
    # now, cdir is the root directory
    return (*cdir['localpath'], *pathparts)


def find_in_dir(dirdict, objname, nickname_first=False):
    """
    Given a directory dict and an objname, return the child dict with the name or nickname of objname,
        along with the list it was found in and the index of the entry in that list.
    If no entry is found, return False, False, False.
    """
    if nickname_first:
        for idx, entry in enumerate(dirdict.get('dir_list')):
            if entry.get('nickname') == objname:
                return entry, 'dir_list', idx
    for idx, entry in enumerate(dirdict.get('dir_list')):
        if entry['name'] == objname:
            return entry, 'dir_list', idx
    for idx, entry in enumerate(dirdict.get('file_list')):
        if entry['name'] == objname:
            return entry, 'file_list', idx
    for idx, entry in enumerate(dirdict.get('dir_list')):
        if entry.get('nickname') == objname:
            return entry, 'dir_list', idx
    return False, False, False


def locate_from_dir(dirdict, objname, nickname_first=False):
    """
    Same as find_in_dir, but handles the case where objname='.' or '..' to return the current/parent directory
    """
    if objname=='.':
        return dirdict, 'dir_list', None
    if objname=='..':
        return dirdict[PARENT], 'dir_list', None
    return find_in_dir(dirdict, objname, nickname_first=nickname_first)


def dict_from_dir_index(dirdict:dict, idx:int):
    """
    Returns a dictionary given its numerical position.
    """
    if idx >= (len(dirdict['dir_list']) + len(dirdict['file_list'])):
        return False, False, False
    if idx >= len(dirdict['dir_list']):
        file_idx = len(dirdict['dir_list'])
        return dirdict['file_list'][idx-file_idx], 'file_list', file_idx
    return dirdict['dir_list'][idx], 'dir_list', idx


def name_from_dir_index(dirdict:dict, idx:int, check_int:bool=True):
    if check_int:
        try:
            idx = int(idx)
        except:
            print('Error: index must be an integer.')
            return False, False, False
    cdir, x_list, idx = dict_from_dir_index(dirdict, idx)
    if not cdir:
        return False, False, False
    return cdir['name'], x_list, idx


def replace_entry_in_dir(direc, new_dict, quiet=False):
    """
    Replaces an "unrecorded" child dict with a "recorded" dict.
    """
    old_dict, x_list, idx = find_in_dir(direc, new_dict['name'])
    if old_dict==False and not quiet:
        print(new_dict['name'] + " not found in directory " + direc['name'])
        return False
    if direc[x_list][idx]['type']=='unrecorded':
        direc[x_list][idx] = new_dict
        direc[x_list][idx][PARENT] = direc
        return True
    else:
        if not quiet:
            print("Entry already recorded.")
        return False


def recursive_dir_list_gen(dictin, only_recorded_dirs=False):
    yield from dir_children_generator(dictin, 
                                      types_to_include=['dir_list'], 
                                      only_recorded_entries=only_recorded_dirs)


def dir_children_generator(dictin:dict, 
                           types_to_include:tuple=['file_list', 'dir_list'], 
                           only_recorded_entries:bool=False):
    yield dictin
    for x_list in types_to_include:
        for entry in dictin.get(x_list, []): # responds correctly to files
            if entry['type']!='unrecorded' or not only_recorded_entries:
                yield from dir_children_generator(entry, types_to_include, only_recorded_entries)


def setup_parents(dictin):
    for entry in recursive_dir_list_gen(dictin, only_recorded_dirs=True):
        for sub_entry in entry['dir_list']+entry['file_list']:
            sub_entry[PARENT] = entry
    return dictin


def dir_is_empty(dictin):
    dirs = [entry['type']=='unrecorded' for entry in dictin['dir_list']]
    files = [entry['type']=='unrecorded' for entry in dictin['file_list']]
    return all(dirs + files)


### Code for moving a file


def bare_move_entry(source_dict:dict, destination_dict:dict) -> bool:
    """
    Code for inserting source_dict into the destination_dict, 
    alphabetizing the children,
    and removing the source_dict from its original parent dict.
    """
    if destination_dict['type'] not in DIR_LIST_TYPES:
        return False
    source_parent = source_dict[PARENT]
    entry, x_list, idx = find_in_dir(source_parent, source_dict['name'])
    destination_dict[x_list].append(source_dict)
    fileobj_alphabetize(destination_dict)
    source_parent[x_list].pop(idx)
    return True


def refresh_entry_paths(dictin:dict, new_root_name:str=None):
    """
    Iteratively goes through every child of dictin, and gives it a path
    based on the path of dictin and on its own path from dictin.
    """
    if dictin['type']==DEVINFO:
        return
    path_walk_gen = dir_children_generator(dictin, only_recorded_entries=True)
    if dictin['type']=='rootdir':
        # this means that dirin is a root, and its parent (devinfo) has no path.
        next(path_walk_gen)
    for entry in path_walk_gen:
        entry['path'] = (*entry[PARENT]['path'], entry['name'])
        if not (new_root_name is None):
            entry['root'] = new_root_name


def move_entry(source_dict:dict, destination_dict:dict, new_name:str=None):
    bare_move_entry(source_dict, destination_dict)
    new_root_name = None
    if new_name:
        source_dict['name'] = new_name
        if source_dict['type']=='rootdir':
            new_root_name = source_dict['name']
    refresh_entry_paths(source_dict, new_root_name)
