# navtuils - utility functions for nagivating tree files
#   and path manipulation.


from treerec.command_parser import Madout
from treerec.primitives import PARENT
from treerec.pathtuputils import *
from treerec.trace_ancestors import find_current_root
from treerec.dirutils import *


class SuperPath():
    def __init__(self, destination_dict):
        self.name = destination_dict['name']
        self.path = destination_dict['path']

        root = find_current_root(destination_dict)

        self.root_nickname = root.get('nickname')
        self.root_path = root['path']
        self.root_localpath = root.get('localpath', ())
        self.after_root = subtract_paths(root['path'], destination_dict['path'])
        self.localpath = (*self.root_localpath, *self.after_root)

    def print_path(self, *additions):
        return combine_pathtuples(self.path, *additions)

    def print_localpath(self, *additions):
        return combine_pathtuples(self.localpath, *additions)

    def print_root_path(self, *additions):
        return combine_pathtuples(self.root_path, *additions)

    def print_root_localpath(self, *additions):
        return combine_pathtuples(self.root_localpath, *additions)

    def print_after_root(self, *additions):
        return combine_pathtuples(self.after_root, *additions)


def get_localpath_from_path(direc):
    """
    Assuming that the 'path' of direc is a treepath,
    find the localpath using its root's localpath.
    """
    root = find_current_root(direc)
    after_root = subtract_paths(root['path'], direc['path'])
    return (*root['localpath'], *after_root)


def get_path_from_localpath(direc):
    """
    Assuming that 'path' of direc is a localpath,
    find the treepath using its root's treepath.
    """
    root = find_current_root(direc)
    after_root = subtract_paths(root['localpath'], direc['path'])
    return (*root['path'], *after_root)


def cd_virt(cdir:dict, dirname:str) -> Madout:
    """Virtual change directory."""

    if dirname=='.':
        return Madout(True, "", cdir)
    if dirname=='..':
        return Madout(True, "", cdir[PARENT])

    entry, list_from, idx = find_in_dir(cdir, dirname)
    if entry==False:
        return Madout(False, "does not exist")
    if list_from=='file_list':
        return Madout(False, "not a directory")
    if list_from=='dir_list':
        if entry['type']=='unrecorded':
            return Madout(False, "not recorded")
        return Madout(True, "", entry)


def find_best_root(devdict:dict, pathtuple:tuple, use_local:bool=False) -> dict:
    """
    Finds the best root of the path: the ancestor root 
        with the most path parts in common.
    If no roots are found, returns the original directory.
    Expects pathtuple to be an absolute path.
    Works even when devdict is not DEVINFO.
    """
    max_similarity_len = 0
    curdir = devdict
    root_path_to_use = ('localpath' if use_local else 'path')
    for rootdir in devdict['dir_list']:
        if is_ancestor(rootdir.get(root_path_to_use, ()), pathtuple) and (len(rootdir.get(root_path_to_use, ())) > max_similarity_len):
            curdir = rootdir
            max_similarity_len = len(rootdir[root_path_to_use])
    return curdir


def get_dict_from_path(head_dict:dict, pathtuple:tuple, use_local:bool=False) -> Madout:
    """
    Returns the dictionary corresponding to the given path.
    Assumes a full absolute path is given.
    Works even if head_dict is not DEVINFO.
    Accounts for root nicknames, but cannot account for paths starting with '.', '..', or '^'.
    """
    path_key = ('localpath' if use_local else 'path')
    rootdir = find_best_root(head_dict, pathtuple, use_local)
    if rootdir==head_dict:
        return Madout(False, "Root not found")
    idx = len(rootdir[path_key])
    mad_curdir = Madout(True, "", rootdir)
    olddir = rootdir
    while idx < len(pathtuple):
        mad_curdir = cd_virt(olddir, pathtuple[idx])
        if not mad_curdir:
            rootpath = combine_pathtuples(rootdir[path_key])
            afterpath = combine_pathtuples((),
                                           subtract_paths(rootdir['path'], olddir['path']),
                                           (pathtuple[idx],))
            return Madout(False, "File (" + rootpath + ") " + afterpath + " not found in tree.")
        olddir = mad_curdir.result()
        idx += 1
    return mad_curdir


def get_dict_from_path_after_start(start_dict, pathtuple, localpath_output=False):
    """
    Traverses path from start_dict, and returns corresponding dict.
    """
    if len(pathtuple)==0:
        return Madout(True, "", start_dict)
    idx = 0
    mad_curdir = Madout(True, "", start_dict)
    olddir = start_dict
    while idx < len(pathtuple)-1:
        mad_curdir = cd_virt(olddir, pathtuple[idx])
        if not mad_curdir:
            SP = SuperPath(olddir)
            failure_path = (SP.print_localpath((pathtuple[idx],)) if localpath_output else SP.print_path((pathtuple[idx],)))
            if mad_curdir.message=='not a directory':
                return Madout(False, "File " + failure_path + ' is not a directory.')
            if mad_curdir.message=='not recorded':
                return Madout(False, "File " + failure_path + ' is not recorded.')
            if mad_curdir.message=='does not exist':
                return Madout(False, "File " + failure_path + ' does not exist.')
            else:
                return Madout(False, "File " + failure_path + ' not found.')
        olddir = mad_curdir.result()
        idx += 1
    last_entry, list_from, ii = locate_from_dir(olddir, pathtuple[idx])
    if last_entry==False:
        return Madout(False, "File " + combine_pathtuples(olddir['path'], (pathtuple[idx],)) + ' not found.')
    return Madout(True, "", last_entry)
