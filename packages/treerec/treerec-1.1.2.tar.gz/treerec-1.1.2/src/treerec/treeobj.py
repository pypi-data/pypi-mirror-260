import json, os, time
from pathlib import *
from treerec.primitives import *
from treerec.hist_events import *
from treerec.dictutils import *
from treerec.pathtuputils import *
from treerec.dirutils import *
from treerec.navutils import *
from treerec.entryutils import *


forbidden_root_nicknames = {
    '.', '..', '^', '^^', '*', '/', '\\'
    }


def active(func):
    def must_be_active_wrapper(trobj, *args, **kwargs):
        if trobj.is_active():
            return func(trobj, *args, **kwargs)
        else:
            print('Tree must be active to perform this operation.')
    return must_be_active_wrapper


def onsystem(func):
    def must_be_onsystem_wrapper(trobj, *args, **kwargs):
        if trobj.onsystem:
            return func(trobj, *args, **kwargs)
        else:
            print('Tree must be on its host system to perform this operation.')
    return must_be_onsystem_wrapper


def unsaved(func):
    def set_unsaved_changes_wrapper(trobj, *args, **kwargs):
        out = func(trobj, *args, **kwargs)
        if out:
            trobj.has_unsaved_changes = True
            trobj.dict['mtime'] = time.time()
        return out
    return set_unsaved_changes_wrapper


def ls_idx_string(idx:int, padding:int=1):
    numstr = str(idx)
    padnum = padding-len(numstr)
    return '[' + (' '*padnum) + numstr + '] '


def ls_dict(dirin:dict, recorded_only:bool=False, show_mtime:bool=False, show_index:bool=False):
    NOTE_IND = '!'
    UNREC_IND = 'x'
    TIE_IND = '='
    ROOT_IND = '<>'
    DIR_IND = '[]'
    FILE_IND = '  '
    padding = len(str(len(dirin['dir_list']) + len(dirin['file_list'])))
    if dirin['type']=='unrecorded':
        print(dirin['name'] + ' is not a recorded directory.')
        return
    if dirin['type'] not in DIR_LIST_TYPES:
        print(dirin['name'] + ' is not a directory.')
        return
    if dirin['type']==DEVINFO:
        for idx, rootentry in enumerate(dirin['dir_list']):
            rootpath = rootentry.get('path', None)
            if rootpath is None:
                pathprint = 'KEY ERROR: "path"'
            elif rootpath==():
                pathprint = '/'
            else:
                pathprint = combine_pathtuples(rootpath)
            root_local_path = rootentry.get('localpath', None)
            if not root_local_path:
                localprint = 'KEY ERROR: "localpath"'
            elif root_local_path==():
                localprint = '/'
            else:
                localprint = combine_pathtuples(root_local_path)
            print( (ls_idx_string(idx, padding) if show_index else ' ') + 
                  (NOTE_IND if len(rootentry.get('notes', []))>0 else ' ') +
                  ' ' + ROOT_IND + ' ' + rootentry.get('nickname', 'ERROR') +
                  '  //  path: (' + pathprint + ')' +
                  '   local: [' + localprint + ']')
        return
    for idx, entry in enumerate(dirin['dir_list']):
        if not (recorded_only and entry['type']=='unrecorded'):
            print( (ls_idx_string(idx, padding) if show_index else ' ') +
                  (TIE_IND if len(entry.get('ties', [])) > 0 else ' ') + 
                  (UNREC_IND if entry['type']=='unrecorded' else 
                    (NOTE_IND if len(entry.get('notes', [])) > 0 else ' ')) +
                  DIR_IND + ' ' + entry['name'] + 
                  ('     ' + time_formatted(entry['mtime']) 
                    if (show_mtime and entry['type']!='unrecorded')
                     else '')
                )
    for idx, entry in enumerate(dirin['file_list']):
        if not (recorded_only and entry['type']=='unrecorded'):
            print( (ls_idx_string(idx + len(dirin['dir_list']), padding) if show_index else ' ') + 
                  (TIE_IND if len(entry.get('ties', [])) > 0 else ' ') + 
                  (UNREC_IND if entry['type']=='unrecorded' else 
                    (NOTE_IND if len(entry.get('notes', [])) > 0 else ' ')) +
                  FILE_IND + ' ' + entry['name'] + 
                  ('     ' + time_formatted(entry['mtime']) 
                    if (show_mtime and entry['type']!='unrecorded')
                    else '')
                )


def print_ties(entry):
    if len(entry['ties'])==0:
        print('>> [ no ties.]')
        return
    for tie in entry['ties']:
        name = tie.get('name', FIELD_NOT_RECORDED)
        device = tie.get('device', FIELD_NOT_RECORDED)
        pathstr = combine_pathtuples(tie.get('path', ()))
        nickname_path = tie.get('nickname_path',())
        root_nickname = ''
        path_after_nickname_str = ''
        tie_time = (time_formatted(tie['time']) if tie.get('time', False) else FIELD_NOT_RECORDED)
        if len(nickname_path)>=1:
            root_nickname = nickname_path[0]
        if len(nickname_path)>=2:
            path_after_nickname_str = combine_pathtuples(nickname_path[1:])
        print( ('* ' if tie.get('identical_hash', False) else '  ') + '>> ' + name + '  <' + device + '>')
        print('   ' + pathstr)
        print('   ' + '(' + root_nickname + ')/' + path_after_nickname_str)
        print('   Session: ' + (tie['session'] if tie['session']!=None else 'None'))
        print('   Time: ' + tie_time)
        print('---------------')
    

def pathtup_without_windows_drive_backslash(pathlike):
    """
    Removes the backslash from the start of a Windows pathlike object.
    """
    if not isinstance(pathlike, PureWindowsPath):
        return pathlike.parts
    drive_name = pathlike.parts[0]
    if len(drive_name)!=0 and drive_name[-1]=='\\':
        drive_pure = drive_name[:-1]
    return (drive_pure, *pathlike.parts[1:])




class TreeObj():
    """
    TreeObj class: fundamental class for holding, manipulating, and displaying tree information.

    Tree must be `active` before any changes can be made of any kind,
    including tying files together, renaming, moving, or deleting files.

    Tree must be `onsystem` before any new directories/files can be recorded.

    The tree is stored as a nested series of dictionaries.
    The top-level dictionary is named DEVINFO (defined in dictutils, defaults to 'devinfo'), and has device information.
    DEVINFO contains directories, called 'roots', which are meant to correspond
    to different drives on a machine. Each root has it's own 'treepath', which
    is what is used to calculate the paths of each of its children.
        - This is so that the paths have a consistent name, even if the drive
        name is not consistent between sessions.
    """

    def __init__(self, device=None, session=None, onsystem=False, owner=None):
        self.onsystem = onsystem
        self.session = session
        self.device = device
        if onsystem:
            self.set_onsystem()
        self._showname = device
        # self.mPath = self.decide_Path()
        self._ACTIVE = False
        self.hash_files = True  # do we compute SHA256 hash when recording files?
        self.auto_update = True  # do we automatically update the listings of directoies that we cd into?
        self.os_type = None  # This allows us to override the recorded os of entries.
        #  This is helpful when accessing NT drives through Linux OS, for instance.
        self.savefile = None
        self.savefile_active = False
        self.has_unsaved_changes = False
        self.dict = create_dict_pure(
                objname=DEVINFO,
                objtype=DEVINFO,
                objpath=('',),
                owner=owner, 
                device=self.device,
                os_type=os.name,
                ctime=int(time.time()),
                mtime=int(time.time()),
                atime=int(time.time()),
                nickname=DEVINFO,
                include_uuid=True
                )
        self.dict[PARENT] = self.dict
        self.dict['history'].append(record_entry(self.dict, session))
        self.CDIR = self.dict
        self.autoupdate_entries = False
        self.ignore_names_list = []
    

    ### Setting and checking basic properties of the system,
    ### such as `active`, `onsystem`, and `savefile`.


    def set_onsystem(self, device:str=None):
        if device:
            self.set_device(device)
        if not self.device:
            print('Please set device name before asserting that the tree is on the system.')
            return
        self.onsystem = True
        print('Tree on system device "' + self.device + '".')
        print('Auto-update is ' + ('on' if self.auto_update else 'off'))
        print('File hashing is ' + ('on' if self.hash_files else 'off'))
        print('Remember to check the local paths of the tree roots, \n'
              ' as they need to reflect the locations of the files on the system.')

    def set_offsystem(self):
        self.onsystem = False

    def activate(self, sessionname:str=None):
        if sessionname:
            self.session = sessionname
        if self.session==None:
            print('Set session name before activating tree.')
            return
        self._ACTIVE = True

    def deactivate(self):
        self._ACTIVE = False

    def is_active(self):
        return self._ACTIVE
    
    def set_showname(self, name):
        self._showname = name

    def set_device(self, devname:str):
        if not dir_is_empty(self.dict):
            print('Device name can only be changed when tree is first created '
                  '(i.e. when there are no roots: the DEVINFO has no children.)')
            return False
        self.device = devname
        self.dict['device'] = devname
        return True

    @unsaved
    def set_savefile(self, filename=None, quiet=False, force=False):
        # This has the @unsaved decorator, because if the Tree is set to a new savefile,
        # it has not been saved to that savefile yet.
        if filename==None:
            if self.savefile!=None:
                print("Setting load file (" + str(self.savefile) + ") as save file...")
                self.savefile_active = True
                return False
            else:
                print("File name not entered.")
                return False
        if os.path.exists(filename):
            if not quiet: print("Warning: save file already exists.")
            if not force:
                if not quiet: print("Save file not changed.")
                return False
        savefile_pathlike = full_Path(filename, verbose=False)
        if not savefile_pathlike:
            if not quiet: print('Error: save file already exists, and cannot be accessed by the System.')
            return False
        self.savefile = savefile_pathlike
        self.savefile_active = True
        print("Save file set to " + str(self.savefile))
        return True

    def set_os_type(self, os_type:str=None):
        if os_type not in ['nt', 'posix', None]:
            print('Unusual OS type... Windows = "nt", Linux/Mac = "posix".')
        self.os_type = os_type 

    def print_os_type(self):
        return (self.os_type if self.os_type else os.name)

    def set_hash_rule(self, do_hash:bool):
        self.hash_files = bool(do_hash)

    def make_settings(self):
        return {
                'hash_files': self.hash_files,
                'auto_update': self.auto_update,
                }

    
    ###   Saving and loading


    def to_json(self, settings:dict=dict(), indent=None):
        return json.dumps({'settings': settings, 'data':self.dict}, skipkeys=True, indent=indent)

    @active
    def save(self, pretty:bool=False):
        if not self.savefile_active:
            print("File saving not activated. Please set a save file.")
            return False
        try:
            with open(self.savefile, mode='w') as fopen:
                indent = ('  ' if pretty else None)
                fopen.write(self.to_json(
                    settings=self.make_settings(),
                    indent=indent
                    ))
                self.has_unsaved_changes = False
                return True
        except Exception as error:
            print(error)
            return False

    def load_dict(self, dictin):
        self.dict = setup_parents(dictin)
        self.onsystem = False
        self._ACTIVE = False
        self.device = self.dict['device']
        self._showname = self.device
        self.CDIR = self.dict
        self.dict['atime'] = int(time.time())
        if dictin['os_type'] != os.name:
            print('WARNING: loaded os type not equal to system os type. Double-check for accuracy.')
            self.set_os_type(dictin['os_type'])

    def load_settings(self, settings_dict):
        """
        Load some values from a settings dict into the tree.
        """
        self.hash_files = settings_dict.get('hash_files', True)
        self.auto_update = settings_dict.get('auto_update', True)

    def load_json_file(self, filename, safe=True):
        pathlike = full_path(filename)
        if not pathlike:
            return
        try:
            with open(pathlike, mode='r') as fopen:
                try:
                    file_dict = json.load(fopen)
                except:
                    print("Error loading json from file " + filename)
                    return
        except Exception as error:
            print('Error opening file ' + filename + ':')
            print(error)
            return
        if not file_dict.get('data', False):
            if file_dict['type']==DEVINFO:
                dictin = file_dict
                settings = dict()
            else:
                print('Error loading file: cannot find DEVINFO of json file.')
                return
            print('Old format file loaded...')
        else:
            dictin = file_dict['data']    
            settings = file_dict['settings']
        self.load_dict(dictin)
        self.load_settings(settings)
        self.savefile = pathlike
        return file_dict.get('settings', None)


    ###   Traversing paths: returning the correct dict given a string


    def ret_root_or_cdir_file_from_path_beginning(self, pathparts) -> tuple[dict, tuple, str]:
        """
        Searches the first entries of pathparts to find a good starting directory for path traversal.
        Returns a dict directory, the pathparts that come after it, and the name of
            the child list that the dict is found in.
        First, if the first entry is '.', return self.CDIR.
        Then, it searches to find a root that's an ancestor.
        Then, it searches the current directory for an object.
        Then, it searches the root nicknames.
        If all fails, return False.
        """
        if len(pathparts)==0:
            return False, False, False
        # Search for ancestor root:
        cdir = find_best_root(self.dict, pathparts)
        if cdir!=self.dict:
            path_after_start = subtract_paths(cdir['path'], pathparts)
            return cdir, path_after_start, 'dir_list'
        # Search inside self.CDIR:
        # locate_from_dir also accounts for '..'
        if pathparts[0]=='.':
            return self.CDIR, pathparts[1:], 'dir_list'
        if pathparts[0]=='..':
            return self.CDIR[PARENT], pathparts[1:], 'dir_list'
        nextdir, x_list, idx = find_in_dir(self.CDIR, pathparts[0])
        if nextdir:     # this means that the path is relative, with no './' at the start.
            return self.CDIR, pathparts, 'dir_list'
        # Search for root nickname:
        nextdir, x_list, idx = find_in_dir(self.dict, pathparts[0], nickname_first=True)
        if nextdir:
            return nextdir, pathparts[1:], x_list
        return False, False, False

    def get_path_initial_dict(self, pathstring:str) -> tuple[dict, tuple]:
        """
        Traverses the input pathstring, and returns the most primitive dict of the path,
            e.g., the root directory (for absolute paths or '^') 
            or the current directory (for relative paths, '.').
        Handles '.', '..', '^', root nicknames, absolute (tree) paths, and relative paths.
        """
        pathstring = pathstring.strip()
        pathparts = PurePosixPath(pathstring).parts
        if len(pathparts)==0:
            return self.CDIR, ()
        elif pathparts[0]=='^':
            # This is the character for the current root.
            if self.CDIR is self.dict:
                print('Error: cannot use "current root" identifier (^) when current directory is DEVINFO.')
                return False, ()
            cdir = find_current_root(self.CDIR)
            path_after_start = pathparts[1:]
        elif pathparts[0]=='^^':
            # This is the character combo for devinfo.
            cdir = self.dict
            path_after_start = pathparts[1:]
        else:
            # Consideres '..', '.', root paths, and root nicknames.
            cdir, path_after_start, x_list = self.ret_root_or_cdir_file_from_path_beginning(pathparts)
            if x_list=='file_list':
                if len(path_after_start)!=0:
                    print('Error: ' + pathparts[0] + ' is a file, not a directory.')
                    return False, ()
                else:
                    return cdir, ()
        if not cdir:
            print('Error: could not find starting directory.')
            return False, ()
        return cdir, path_after_start
        # Now, we traverse the path
    
    def traverse_path(self, pathstring:str) -> dict:
        cdir, path_after_start = self.get_path_initial_dict(pathstring)
        if len(path_after_start)==0:
            return cdir
        mad_cdir = get_dict_from_path_after_start(cdir, path_after_start)
        if not mad_cdir:
            print(mad_cdir)
            return False
        return mad_cdir.result()
    
    def get_parent_of_path_file(self, pathstring:str) -> dict:
        cdir, path_after_start = self.get_path_initial_dict(pathstring)
        if not cdir:
            return False
        if len(path_after_start)==0:
            # e.g. path points to '.', '..', a root, etc.
            return cdir.get(PARENT, None)
        mad_cdir = get_dict_from_path_after_start(cdir, path_after_start[:-1])
        if not mad_cdir:
            print(mad_cdir)
            return False
        return mad_cdir.result()
        
    
    ###   Unix-like commands for viewing and changing directories


    def ls(self, dirpath:str=None, recorded_only:bool=False, show_mtime:bool=False, show_index:bool=False):
        if not dirpath:
            dirin = self.CDIR
        else:
            dirin = self.traverse_path(dirpath)
        if not dirin:
            return
        if dirin['type'] not in DIR_LIST_TYPES:
            print('Error: cannot list contents of a non-directory.')
            return
        if self.onsystem and self.auto_update and (self.CDIR is not self.dict):
            update_unrecorded_contents(self.CDIR, quiet=True)
        ls_dict(dirin, recorded_only, show_mtime, show_index=show_index)

    def lsroots(self):
        ls_dict(self.dict)

    def roots(self):
        ls_dict(self.dict)

    def cd_cdir(self, dirname):
        """
        Old version, withou using self.traverse_path
        """
        if self.CDIR['type']==DEVINFO:
            self.chroot(dirname)
            return
        newdir_out = cd_virt(self.CDIR, dirname)
        if not newdir_out:
            if newdir_out.message=="does not exist":
                print(dirname + " does not exist in the current directory.")
            elif newdir_out.message=="not a directory":
                print(dirname + " is not a directory.")
            elif newdir_out.message=="not recorded":
                print(dirname + " must be recorded before it can be accessed.")
            return
        self.CDIR = newdir_out.result()

    def cd(self, dirpath:str, use_index:bool=False):
        if use_index:
            try:
                dir_idx = int(dirpath)
                newdir_out, _, _ = dict_from_dir_index(self.CDIR, dir_idx)
            except:
                print('Error: entry index must be an integer.')
                return False
        else:
            newdir_out = self.traverse_path(dirpath)
        if not newdir_out:
            return False
        if newdir_out['type']=='unrecorded':
            print(dirpath + " must be recorded before it can be accessed.")
            return False
        if newdir_out['type'] not in DIR_LIST_TYPES:
            print(dirpath + " is not a directory.")
            return False
        self.CDIR = newdir_out
        return True

    def chroot(self, rootname):
        for entry in self.dict['dir_list']:
            if entry.get('nickname')==rootname:
                self.CDIR = entry
                return
        print(rootname + " is not the nickname of any root.")
        return

    def pwd(self, full=False):
        SP = SuperPath(self.CDIR)
        print(self._showname + ": (" +
              (SP.print_root_path() if full in ['tree', 'treepath']
               else SP.print_root_localpath() if full in ['local', 'localpath']
               else SP.root_nickname) +
             ")/" + SP.print_after_root())


    ###    Recording new entries


    @onsystem
    @active
    @unsaved
    def recroot(self, root_localpath:str, nickname:str=None, treepath:str=None):
        """
        Create new root entry in the `dirinfo` directory.
        """
        root_localpathlike = full_Path(root_localpath)
        if not root_localpathlike:
            return False
        if not valid_dir(root_localpathlike, verbose=True):
            print('Root directory must be a directory.')
            return False
        if nickname in forbidden_root_nicknames:
            print('Cannot use "' + nickname + '" as a Root Nickname.')
            return False
        if nickname=='':
            print('You cannot have an empty Root Nickname.')
            return False
        if nickname==None:
            print('You should really set a Nickname manually...')
            if root_localpathlike.name in forbidden_root_nicknames:
                print('Cannot use file''s name, "' + root_localpathlike.name +
                      '", to be the Root Nickname. Please choose another Nickname.')
                return False
            nickname = root_localpathlike.name
        if '/' in nickname or '\\' in nickname:
            print('Nickname cannot include "/" or "\\".')
            return False
        current_root_names = [entry['nickname'] for entry in self.dict['dir_list']]
        if nickname in current_root_names:
            print('Root with Nickname "' + nickname + '" already exists.')
            return False
        if treepath==None:
            treepath_tup = pathtup_without_windows_drive_backslash(root_localpathlike)
        elif treepath=='':
            print('Root cannot have an empty Tree path.')
            return False
        elif type(treepath) is tuple:
            treepath_tup = treepath
        else:
            treepath_tup = PurePosixPath(treepath).parts
        if treepath_tup==():
            print('Root cannot have an empty Tree path.')
            return False
        current_root_treepaths = [entry['path'] for entry in self.dict['dir_list']]
        if treepath_tup in current_root_treepaths:
            print('Root with Tree path ' + combine_pathtuples(treepath_tup) + ' already exists.')
            return False
        newentry = create_dict(
            root_localpathlike, 
            rootname=nickname, 
            device=self.device,
            nickname=nickname, 
            session=self.session, 
            do_hash=self.hash_files
            )
        newentry['localpath'] = root_localpathlike.parts
        newentry['path'] = treepath_tup
        newentry[PARENT] = self.dict
        newentry['type'] = 'rootdir'
        self.dict['dir_list'].append(newentry)
        return True

    @active
    @unsaved
    def root_set_treepath(self, rootname:str, recpath:str):
        """
        Set the tree (record) path of a root, i.e. the path which is recorded in the tree to it and its descendants.
        This is static, and can only be set once, when the root has no recorded files.
        Really, this should be set when first recording the tree (using self.recroot())
        """
        if rootname=='^':
            root = find_current_root(self.CDIR)
        else:
            root, _, _ = find_in_dir(self.dict, rootname, nickname_first=True)
        if not root:
            print("Root " + rootname + " not found.")
            return False
        if not dir_is_empty(root):
            print('Root must be empty before setting record path (treepath).')
            return False
        if root['type']==DEVINFO:
            print("Cannot set treepath on DEVINFO, only Roots.")
            return False
        pathparts = PurePosixPath(recpath.strip()).parts
        current_tree_paths = [entry['path'] for entry in self.dict['dir_list']]
        if pathparts in current_tree_paths:
            print('Root with tree path ' + combine_pathtuples(pathparts) + ' already exists.')
            return False
        root['path'] = pathparts
        return True
    
    def root_set_localpath(self, rootname:str, localpath:str):
        """
        Set the local path of a root, i.e. the path on the host system to the root folder.
        We expect the local path of the root to change often, especially for an archival drive,
            which will be connected to many devices in order to record them.
        """
        if rootname=='^':
            root = find_current_root(self.CDIR)
        else:
            root, _, _ = find_in_dir(self.dict, rootname)
        if not root:
            print("Root " + rootname + " not found.")
            return
        if root['type']==DEVINFO:
            print('Cannot set localpath for DEVINFO, only for Roots.')
            return
        localpathlike = full_Path(localpath.strip())
        if not localpathlike:
            return
        pathparts = localpathlike.parts
        current_local_paths = [entry['localpath'] for entry in self.dict['dir_list']]
        if pathparts in current_local_paths:
            print('Root with local path ' + combine_pathtuples(pathparts) + ' already exists.')
            return
        root['localpath'] = pathparts

    @onsystem
    @active
    @unsaved
    def record(self, objname:str, cdir:dict=None, quiet:bool=False) -> bool:
        """
        Very basic record function. Does not support path entries.
        Should not be called by the user.
        Records <objname> from inside <cdir>.

        Notes: (on Windows)
            - Path(file) does not update st_atime
            - os.stat(file) does note update st_atime
        """
        if cdir==None:
            cdir = self.CDIR
        if cdir['type']=='unrecorded':
            print(cdir['name'] + " must be recorded before its contents can be accessed.")
            return False
        return new_entry_in_dir(
            cdir,
            objname,
            device=self.device,
            os_type=self.os_type,
            session=self.session,
            quiet=quiet,
            do_hash=self.hash_files
            )

    @onsystem
    @active
    def rec(self, pathstr:str, verbose:bool=False, quiet:bool=False) -> bool:
        """
        Path RECord:
        Record file, given absolute path tuple (treepath)
        Uses treepath, not localpath
        """
        parent_dict = self.get_parent_of_path_file(pathstr)
        if not parent_dict:
            return False
        if parent_dict==self.dict:
            print('Cannot record files in DEVINFO. Use recroot to record a new root directory.')
            return False
        objname = PurePosixPath(pathstr).name
        if verbose: print('R:   ' + combine_pathtuples(parent_dict.get('path', ('',)), (objname,)))
        return self.record(objname, parent_dict, quiet=quiet)

    @onsystem
    @active
    def lrec(self, pathin:str, verbose:bool=False, quiet:bool=False) -> bool:
        """
        Local RECord:
        Records file, given absolute pathlike (local path) object.
        We first search through the trees' local paths to find the best root.
        Then, we replace the root's local path in the input path with its tree path,
            traverse through the tree's directory structure, and record the file.
        """
        if type(pathin) is Path:
            pathtuple = pathin.parts
        elif type(pathin) is tuple:
            pathtuple = pathin
        elif type(pathin) is str:
            pathin_pathlike = full_Path(pathin)
            if not pathin_pathlike:
                return False
            pathtuple = pathin_pathlike.parts
        else:
            print("Error: path must be a string, Path, or path tuple.")
            return False
        mad_parent_dict = get_dict_from_path(self.dict, pathtuple[0:-1], use_local=True)
        if not mad_parent_dict:
            print(mad_parent_dict)
            return False
        return self.record(pathtuple[-1], mad_parent_dict.result(), quiet=quiet)

    @onsystem
    @active
    def arec(self, cdir:dict=None, verbose:bool=False, head_path:list=[], global_ignore:list=[], quiet:bool=True) -> None:
        """
        All RECord:
        Record all files in directory.
        """
        if cdir==None:
            cdir = self.CDIR
        if cdir['name'] in self.ignore_names_list+global_ignore:
            return
        if verbose: print('R: >>> ' + combine_pathtuples(('*',), subtract_paths(head_path, cdir.get('path', ('',)))))
        for entry in cdir['dir_list']+cdir['file_list']:
            if entry['name'] not in self.ignore_names_list+global_ignore:
                if verbose: print('R:   ' + combine_pathtuples(('*',), subtract_paths(head_path, cdir.get('path', ('',))), (entry['name'],)))
                self.record(entry['name'], cdir, quiet=quiet)

    @onsystem
    @active
    def rrec(self, dirpath:str='.', levels:int=0, global_ignore:list=[], verbose_levels:int=0, quiet:bool=True) -> bool:
        """
        Recursive RECord.
        levels=0 is identical to self.rec [FILE].
        levels=1 is identical to self.arec [DIR].
        levels<0 will record all possible subdirectories.
        """
        cdir = self.traverse_path(dirpath)
        if not cdir: return False
        if cdir['type']==DEVINFO:
            print("Cannot execute recursive record on DEVINFO; must choose root (or regular) directory.")
            return False
        if cdir['type']=='unrecorded':
            self.rec(dirpath, quiet=quiet)
            cdir = self.traverse_path(dirpath)
        if verbose_levels: 
            print('R:   ' + combine_pathtuples(cdir.get('path', ('',))))
            verbose_levels -= 1
        if levels==0: return False
        if cdir['type'] not in DIR_LIST_TYPES:
            print("Cannot execute recursive record on a file; must be a recorded directory.")
            return False
        self.recursive_record(cdir, levels=levels-1, global_ignore=global_ignore, verbose_levels=verbose_levels, head_path=cdir['path'], quiet=quiet)
        return True

    def recursive_record(self, cdir, levels=0, verbose_levels:int=0, global_ignore:list=[], head_path:list=[], quiet=True):
        if verbose_levels:
            verbose = True
            verbose_levels -= 1
        else:
            verbose = False
        self.arec(cdir, global_ignore=global_ignore, verbose=verbose, head_path=head_path, quiet=quiet)
        if levels != 0:
            for entry in cdir['dir_list']:
                if entry['name'] not in self.ignore_names_list+global_ignore:
                    self.recursive_record(entry, levels=levels - 1, global_ignore=global_ignore, verbose_levels=verbose_levels, head_path=head_path, quiet=quiet)

    @active
    @unsaved
    def remove(self, objpath:str='.', quite:bool=False):
        """
        Removes a recorded file/directory.
        """
        entry = self.traverse_path(objpath)
        if not entry:
            return False
        if entry['type']==DEVINFO:
            print('Cannot remove DEVINFO.')
            return False
        if entry['type']=='rootdir':
            idx, x_list = get_position_in_parent(entry, nickname_first=True)
            if not x_list:
                return False
            parent = entry[PARENT]
            parent[x_list].pop(idx)
            return True
        else:
            idx, x_list = get_position_in_parent(entry, nickname_first=True)
            if not x_list:
                return False
            unrecorded = {
                'name': entry['name'],
                'type': 'unrecorded'
            }
            parent = entry[PARENT]
            parent[x_list][idx] = unrecorded
            return True
    
    ### Ignorelist manipulation
        
    def ignorelist_print(self):
        for idx, name in enumerate(self.ignore_names_list):
            print('[', idx, ']' + '  ' + name)
    
    def ignorelist_remove(self, name:str=None, idx:int=None):
        if name:
            for ii, entry in enumerate(self.ignore_names_list):
                if entry==name:
                    self.ignore_names_list.pop(ii)
                    return True
            print('Name "' + name + '" not found in Ignore List.')
            return False
        elif idx is not None:
            if idx >= len(self.ignore_names_list):
                print('Error: index (' + idx + ') too large for Ignore List.')
                return False
            self.ignore_names_list.pop(idx)
            return True
        else:
            print('Invalid input for ignorelist_remove')
            return False
    
    def ignorelist_add(self, name:str=None):
        if not name:
            print('Ignore List name cannot be empty.')
            return False
        self.ignore_names_list.append(name)
        return True


    ### Update files
        

    @onsystem
    def update(self, objpath:str='.', quiet:bool=False):
        entry = self.traverse_path(objpath)
        if not entry:
            return
        if entry['type']==DEVINFO:
            print('Cannot update DEVINFO: no corresponding system file.')
            return
        _, updated = update_object(
                entry, 
                session=self.session,
                do_hash=self.hash_files,
                quiet=quiet)
        if updated:
            self.has_unsaved_changes = True

    @onsystem
    def update_contents(self, objpath:str='.', quiet:bool=False):
        dir_dict = self.traverse_path(objpath)
        if dir_dict['type']==DEVINFO:
            print('Cannot update contents of DEVINFO.')
            return
        update_unrecorded_contents(dir_dict, quiet=quiet)

    @onsystem
    @active
    def r_update(self, objpath:str='.', levels:int=0):
        """
        Recursive update: update folder and all children,
        up to a certain number of levels.
        r_update('.', levels=0) updates all entries in directory.
        """
        cdir = self.traverse_path(objpath)
        self.update(objpath)
        updated = self.recursive_update(cdir, levels)
        if updated:
            self.has_unsaved_changes = True

    def recursive_update(self, cdir, levels:int=0):
        if cdir['type']=='unrecorded':
            return False
        updated = False
        for entry in cdir['dir_list']:
            _, tempu = update_object(entry, session=self.session)
            updated = any([updated, tempu])
        for entry in cdir['file_list']:
            _, tempu = update_object(entry, session=self.session)
            updated = any([updated, tempu])
        if levels==0:
            return
        for direc in cdir.get('dir_list', []):
            tempu = self.recursive_update(direc, levels=levels-1)
            updated = any([updated, tempu])
        return updated

    @active
    @unsaved
    def add_note(self, objpath, note_text):
        entry = self.traverse_path(objpath)
        if not entry:
            return False
        return dict_add_note(entry, note_text, session=self.session)

    @active
    @unsaved
    def remove_note(self, objpath, note_idx):
        entry = self.traverse_path(objpath)
        if not entry:
            return False
        try:
            entry['notes'].pop(note_idx)
            return True
        except IndexError:
            print("Note # " + str(note_idx) + " out of range.")
            return False


    ### Manipulate present data
        
    @active
    @unsaved
    def move(self, sourcepath:str, destinationpath:str):
        pass


    ### Print information about entries


    def info(self, objpath, option='full'):
        entry = self.traverse_path(objpath)
        if not entry:
            return
        print()
        if option=='full':
            print_dict_info(entry)
        if option=='short':
            print_dict_info(entry,
                            ('nicknamepath','ctime','mtime','atime','abbrev-hash',
                             'notes','ties','history','lastmodifiedsession'))

    def history(self, objpath:str, full=False):
        entry = self.traverse_path(objpath)
        if not entry:
            return
        if not full:
            print()
            print_dict_history(entry)
        else:
            print()
            print_dict_history_full(entry)

    def notes(self, objpath):
        entry = self.traverse_path(objpath)
        if not entry:
            return
        print()
        print_dict_notes(entry)

    def ties(self, objpath:str):
        entry = self.traverse_path(objpath)
        if not entry:
            return
        print()
        print_ties(entry)


if __name__=='__main__':
    T = TreeObj(device='Test', onsystem=True, owner='Nerneg', session="Test1")
    T.activate()
    T.recroot(Path('..').resolve(), 'rootdir')
    T.rrec(levels=5, quiet=False)
    print()
