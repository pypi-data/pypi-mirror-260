# Path Tuple Utilities - functions for manipulating pathtuples,
# where each entry is a directory/file name.
# Implicity uses pathlib.Path objects, but calls no constructors.


def combine_pathtuples(*pathtuples):
    if len(pathtuples)==0:
        return ''
    if len(pathtuples[0])==0:
        outstr = ['']
    else:
        outstr = ["" if pathtuples[0][0]=='/' else (pathtuples[0][0])]
    outstr.extend(pathtuples[0][1:])
    for pathpiece in pathtuples[1:]:
        outstr.extend(pathpiece)
    if outstr==['']:
        return '/'
    return '/'.join(outstr)


def split_pathstr(pathstr, split_on=['/', '\\']):
    pathlist = [pathstr]
    for split_char in split_on:
        newlist = []
        for entry in pathlist:
            newlist.extend(entry.split(split_char))
        pathlist = newlist
    if pathlist[0]=='':
        pathlist[0] = '/'
    return pathlist


def compare_paths(pathtuple1, pathtuple2):
    """
    Finds how many starting entries in pathtuple1 are identical to those in pathtuple2.
    This function is reflexive.
    pathtuple[idx] is the first element where the paths differ.
    """
    idx = 0
    minlength = min(len(pathtuple1), len(pathtuple2))
    while (idx < minlength) and (pathtuple1[idx] == pathtuple2[idx]):
        idx += 1
    return idx


def subtract_paths(shorttup, longtup):
    if len(shorttup)>len(longtup):
        print("Subtracted path must not be longer than the other path.")
        return False
    idx = compare_paths(shorttup, longtup)
    return longtup[idx:]


def is_ancestor(pathtuple1, pathtuple2):
    """
    Checks if pathtuple1 is an ancestor of pathtuple2.
    This function is not reflexive.
    """
    return (compare_paths(pathtuple1, pathtuple2) == len(pathtuple1))


