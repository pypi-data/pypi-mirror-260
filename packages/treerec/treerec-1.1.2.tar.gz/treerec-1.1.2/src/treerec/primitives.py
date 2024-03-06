# File for declaring primitive values for treerec.

VERSION_NUMBER = '1.1.2'


# ('parent',) is used as the dictionary key for a dict's parent,
# mostly so that it can be automatically removed when converting the
# tree into json by using json.dumps(skipkeys=True).
# If we did not remove them, then we would have infinite recursion.

PARENT = ('parent',)


# DEVINFO is the name, nickname, and type of the top-level dictionary,
# which contains all of the tree children, along with device info.

DEVINFO = 'DEVINFO'


# these are the types of objects which go under the 'dir_list' and
# 'file_list' lists of directory entries, respectively.

DIR_LIST_TYPES = [DEVINFO, 'rootdir', 'dir', 'shortcut']
FILE_LIST_TYPES = ['file']


# This is the default character to represent the system

DEFAULT_SYSCHAR = '$'


# This is the default entry for a printed field when
# the field does not exist.

FIELD_NOT_RECORDED = '---'


# This is the default entry for any printed hash field
# when the file in question is a directory

NO_HASH_BC_DIR = '-(dir)-'


# This is the default entry for a file where the hash
# is not present due to a lack of file permissions

NO_HASH_BC_PERMISSIONS = '-(denied)-'


# Format string for printing dates & times

DATE_FORMAT = '%d/%b/%Y'

TIME_FORMAT = '%I:%M %p'
