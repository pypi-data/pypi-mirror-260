from treerec.primitives import DEVINFO

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
