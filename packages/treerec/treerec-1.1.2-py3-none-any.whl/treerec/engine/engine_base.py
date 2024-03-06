import json, os
from treerec.primitives import *
from treerec.dictutils import *
from treerec.dirutils import name_from_dir_index, full_Path
from treerec.entryutils import time_formatted, tie_files, print_os_file_info
from treerec.treeobj import TreeObj, ls_idx_string


forbidden_tree_nicknames = ['*', '', ' ', DEFAULT_SYSCHAR, '.', '..', '/', '\\', '^', '^^']

def checkname(allowsys=False, replace=True):
    """
    Decorator method for checking if a Tree name is valid.
    If the Tree name is valid, the method is passed through.
    If the Tree name is None, it replaces it with the current Tree,
        unless replace=False, in which case it prints an error message.
    If the Tree name is invalid, it prints an error message, and passes.
    """
    def checkname_decorator(func):
        def checkname_wrapper(mth, treename=None, *args, **kwargs):
            if (treename is None) and replace:
                if mth.CTREE==None:
                    print('No trees in current session.')
                    return None
                treename = mth.CTREE
            if treename==mth.SYSCHAR and not allowsys:
                print('Cannot use this method on the system.')
                return None
            if (treename != mth.SYSCHAR) and (mth.treedict.get(treename) == None):
                print('Tree "' + treename + '" does not exist.')
                return None
            return func(mth, treename, *args, **kwargs)
        return checkname_wrapper
    return checkname_decorator


def accept_index(func):
    """
    Wrapper function for index-based item selection.
    Use:
        Functions with definitions starting as
            func(self, treename, path, ...)
        Should be wrapped with this, and called with
            func(treename, path, use_index, ...)
        Then, if use_index==True, path will be interpreted as an integer index,
          be replaced with the name of the entry at that index,
          and passed to func()
    """
    def accept_index_wrapper(mth, treename, path, use_index, *args, **kwargs):
        if use_index:
            try:
                idx = int(path)
            except:
                print('Error: index must be an integer.')
                return False
            path, _, _ = name_from_dir_index(mth.treedict[treename].CDIR, idx)
            if not path:
                print('Error: index not found.')
                return False
        return func(mth, treename, path, *args, **kwargs)
    return accept_index_wrapper


def os_sorted_lists(pathstr:str='.'):
    pathlike = full_Path(pathstr)
    if not pathlike:
        return False, False
    if not pathlike.exists():
        print('Error locating path ' + str(pathlike))
        return False, False
    try:
        entrylist = os.listdir(pathstr)
    except PermissionError:
        print("Permission denied.")
        return False, False
    except:
        print("Unable to complete request.")
        return False, False
    dir_list = [entry for entry in entrylist if valid_dir(Path(pathlike/entry), verbose=True)]
    file_list = [entry for entry in entrylist if not valid_dir(Path(pathlike/entry), verbose=False)]
    dir_sorted = sorted(dir_list, key=lambda x: str.casefold(x))
    file_sorted = sorted(file_list, key=lambda x: str.casefold(x))
    return dir_sorted, file_sorted


def ls_os(pathstr:str=None, show_index:bool=False, show_mtime:bool=False):
    DIR_IND = '[]'
    FILE_IND = '  '
    if not pathstr:
        pathstr = '.'
    pathlike = full_Path(pathstr)
    if not pathlike:
        return
    dir_sorted, file_sorted = os_sorted_lists(pathstr) 
    padding = len(str(len(dir_sorted) + len(file_sorted)))
    for idx, entry in enumerate(dir_sorted):
        time_str = ('     ' + time_formatted(Path(pathlike/entry).stat().st_mtime) if show_mtime else '')
        index_str = (ls_idx_string(idx, padding) if show_index else ' ')
        print(index_str + '  ' + DIR_IND + ' ' + entry +  time_str)
    for idx, entry in enumerate(file_sorted):
        time_str = ('     ' + time_formatted(Path(pathlike/entry).stat().st_mtime) if show_mtime else '')
        index_str = (ls_idx_string(idx+len(dir_sorted), padding) if show_index else ' ')
        print(index_str + '  ' + FILE_IND + ' ' + entry + time_str)


def name_from_os_dir_index(idx:int):
    dir_sorted, file_sorted = os_sorted_lists('.')
    if idx>=len(dir_sorted):
        if idx>=(len(dir_sorted) + len(file_sorted)):
            print('Error: index (', idx, ') out of range.')
            return None
        return file_sorted[idx-len(dir_sorted)]
    return dir_sorted[idx]

class TreeEngine_Base():

    # These two are here to prevent error messages in Jupyter;
    # they are unused in the code
    shape = ()
    __len__ = lambda self: len(self.treedict)

    def __init__(self, session:str=None):
        self.session = session
        self.ignore_names_list = []
        self.treedict = {}
        self.SYSCHAR = DEFAULT_SYSCHAR
        self.CTREE = self.SYSCHAR

    def __getattr__(self, attr):
        """
        Non-MultiTreeHolder methods are passed through to the current tree.
        """
        if self.CTREE == None:
            print('>>> ' + attr + ' <<<')
            print('No tree is currently active.')
            return self.blankfunc
        if self.CTREE == self.SYSCHAR:
            print('Cannot call method or attribute "' + attr + '" on the system.')
            return self.blankfunc
        tree = self.treedict[self.CTREE] #  Without this declaration, the kernal crashes...
        return getattr(tree, attr)

    def blankfunc(self, *args, **kwargs):
        return None


    ### code for setting tree properties
    ### i.e. onsystem, active, savefile, session


    @checkname(allowsys=False, replace=True)
    def set_onsystem(self, treename:str=None, device:str=None):
        self.treedict[treename].set_onsystem(device=device)

    @checkname(allowsys=False, replace=True)
    def set_offsystem(self, treename:str=None):
        self.treedict[treename].set_offsystem()

    @checkname(allowsys=False, replace=True)
    def activate(self, treename:str=None):
        if not self.session:
            print('Set Session name before activating any trees.')
        self.treedict[treename].activate(self.session)

    @checkname(allowsys=False, replace=True)
    def deactivate(self, treename:str=None):
        self.treedict[treename].deactivate()

    @checkname(allowsys=False, replace=True)
    def set_hash_rule(self, treename:str=None, do_hash:bool=True):
        """Sets the hash rule: whether to hash files when recording onto the Tree."""
        self.treedict[treename].set_hash_rule(do_hash)

    @checkname(allowsys=False, replace=True)
    def set_auto_update(self, treename:str=None, action:bool=False):
        TREE = self.treedict[treename]
        TREE.auto_update = bool(action)
        self.show_auto_update(treename)
        if TREE.auto_update and not TREE.onsystem:
            print('Warning: "' + treename + '" is not on-system, and will not update directory contents.')

    @checkname(allowsys=False, replace=True)
    def show_auto_update(self, treename:str=None):
        print('Autoupdate is ' + 
                ('on' if self.treedict[treename].auto_update else 'off') + 
                ' for Tree "' + treename + '".')

    @checkname(allowsys=False, replace=True)
    def set_savefile(self, treename:str, filename:str, quiet:bool=False, force:bool=False):
        self.treedict[treename].set_savefile(filename, quiet, force)

    @checkname(allowsys=False, replace=True)
    def save(self, treename:str=False, force:bool=True, pretty:bool=False):
        """
        Save the Tree to its Savefile.
        If Tree has no unsaved changes, we do not save unless force=True.
        force=True won't save if there is no Savefile set (Tree.savefile_active == False)
          or if the Tree is not active.
        """
        if not self.treedict[treename].savefile_active:
            print('Warning: Tree not saved. "' + treename + '" has no valid save file.')
            return False
        if not self.treedict[treename].has_unsaved_changes and not force:
            print('Tree "' + treename + '" has no unsaved changes, and will not be saved. Override this with the -f flag.')
            return False
        if not self.treedict[treename].is_active():
            print('Tree "' + treename + '" must be active to perform this operation')
            return False
        saved = self.treedict[treename].save(pretty=pretty)
        if saved:
            print('Tree "' + treename + '" saved...')
            return True
        else:
            return False

    def saveall(self, force:bool=True, pretty:bool=False):
        for treename in self.treedict:
            if self.treedict[treename].has_unsaved_changes or force:
                # The extra condition here prevents the "no unsaved changes" response
                # from popping up on the unsaved trees.
                self.save(treename, force=force, pretty=pretty)

    def has_unsaved(self):
        for treename in self.treedict:
            if self.treedict[treename].has_unsaved_changes:
                return True
        return False

    def set_session_name(self, name:str):
        self.session = name
        self.update_tree_session_names()

    def update_tree_session_names(self):
        for tree in self.treedict.values():
            tree.session = self.session

    def check_nickname_is_valid(self, nickname:str=None):
        if not nickname:
            print('Error: Tree Nickname cannot be blank.')
            return False  
        if '/' in nickname or '\\' in nickname:
            print('Error: forbidden Tree Nickname. Nicknames cannot include "/" or "\\".')
            return False
        if nickname in forbidden_tree_nicknames:
            print('Error: forbidden Tree Nickname.')
            return False
        return True

    @checkname(allowsys=False, replace=True)
    def rename(self, oldname: str, newname: str):
        if not self.check_nickname_is_valid(newname):
            return
        if self.treedict.get(newname) != None:
            print('Error: cannot rename. Tree with name "' + newname + '" already exists.')
            return
        self.treedict[newname] = self.treedict.pop(oldname)
        if self.CTREE == oldname:
            self.CTREE = newname
        print('Tree "' + oldname + '" renamed to "' + newname + '".')


    ### Adding TreeObjs to the MultiTreeHolder


    def add_tree_obj(self, treeobj:TreeObj, nickname:str=None):
        if not self.check_nickname_is_valid(nickname):
            return
        if self.treedict.get(nickname, None):
            print('Tree with name "' + nickname + '" already in session. Use "droptree" to drop this tree or "rename" to rename it.')
            return False
        treeobj.deactivate()
        treeobj.set_offsystem()
        treeobj.session = self.session
        self.treedict[nickname] = treeobj
        if (self.CTREE==None) or (self.CTREE == self.SYSCHAR):
            self.CTREE = nickname
        return True

    def load_tree_file(self, filename:str):
        pathlike = full_Path(filename)
        if not pathlike:
            return False
        if not pathlike.exists():
            print('Error locating file ' + str(pathlike))
            return False
        try:
            with open(filename, mode='r') as fopen:
                try:
                    file_dict = json.load(fopen)
                except:
                    print('Error opening file ' + filename)
                    return False
        except Exception as error:
            print(error)
            return False
        T = TreeObj()
        if not file_dict.get('data', False):
            if file_dict['type']==DEVINFO:
                dictin = file_dict
                settings = dict()
            else:
                print('Error loading file: cannot find DEVINFO of json file.')
                return
            print('Old format file loaded.')
        else:
            dictin = file_dict['data']
            settings = file_dict['settings']
        T.load_dict(dictin)
        T.load_settings(settings)
        T.set_savefile(filename, quiet=True, force=True)
        T.has_unsaved_changes = False  
            # we loaded from this file, so we know the info is there
        return T

    def load_tree(self, filename:str, nickname:str=None):
        T = self.load_tree_file(filename)
        if not T:
            return False
        if nickname == None:
            nickname = T.dict['device']
        self.add_tree_obj(T, nickname=nickname)
        return True

    def new_tree(self, filename:str, device:str, nickname:str=None):
        T = TreeObj(session=self.session, onsystem=False, device=device)
        T.set_savefile(filename)
        if not nickname:
            nickname = T.dict['device']
        T.has_unsaved_changes = True
        self.add_tree_obj(T, nickname=nickname)

    @checkname(allowsys=False, replace=False)
    def droptree(self, treename:str=None, force:bool=True):
        if not self.treedict[treename].has_unsaved_changes or force:
            self.treedict.pop(treename)
            print("Tree " + treename + " dropped...")
            if self.CTREE==treename:
                self.CTREE = self.SYSCHAR
            return True
        else:
            print("Error: Tree has unsaved changes.")
            print('Use the -f flag to force the drop.')
            return False


    ### Basic Unix-like commands for trees

    @checkname(allowsys=True, replace=True)
    def index_to_name(self, treename:str=None, index:int=None):
        if index is None:
            print('Error: index must be an integer.')
            return None
        try:
            idx = int(index)
        except:
            print('Error: index must be an integer.')
            return None
        if treename==self.SYSCHAR:
            name = name_from_os_dir_index(idx)
        else:
            name, _, _ = name_from_dir_index(self.treedict[treename].CDIR, idx)
            if not name:
                print('Error: index not found.')
                return None
        return name

    @checkname(allowsys=True, replace=True)
    def ls_tree(self, treename:str=None, path:str=None, recorded_only:bool=False, show_mtime:bool=False, print_index:bool=False):
        if treename==self.SYSCHAR:
            ls_os(path, print_index, show_mtime)
        else:
            self.treedict[treename].ls(path, recorded_only, show_mtime, print_index)

    def pwt(self):
        """Print Working Tree"""
        if self.CTREE == None:
            print('No tree is currently active.')
            return
        elif self.CTREE == self.SYSCHAR:
            print('Currently on System.')
        else:
            print('Current Tree: ' + self.CTREE)

    @checkname(allowsys=True, replace=True)
    def pwd(self, treename:str=None, full:bool=False):
        if treename==self.SYSCHAR:
            print(os.getcwd())
        else:
            self.treedict[treename].pwd(full)

    @checkname(allowsys=True, replace=True)
    def print_tree(self, treename:str=None, print_session=True):
        if treename==self.SYSCHAR:
            print('>> System')
            return
        indicator = (">> " if self.CTREE==treename else "   ")
        device = self.treedict[treename].dict.get('device', 'N/A')
        hash_file = ("Yes" if self.treedict[treename].hash_files else "No")
        session = (self.treedict[treename].session if self.treedict[treename].session else 'None')
        savefile = (self.treedict[treename].savefile if self.treedict[treename].savefile else 'None')
        print()
        print(indicator +
              'Nickname: ' + treename + '\n' +
              "   Device: " + (device if device!=None else 'N/A') + '\n' +
              "   Last Modified: " + time_formatted(self.treedict[treename].dict['mtime']) + '\n' + 
              "   Hash files?: " + hash_file + '\n' + 
              "   Save File: " + str(savefile) + '\n' +
              (('   Session: ' + session) if print_session else ''))

    def list_trees(self):
        print()
        print('Session: ' + (self.session if self.session else 'None'))
        for treename in self.treedict:
            self.print_tree(treename, print_session=False)
    
    @checkname(allowsys=False, replace=True)
    def print_savefile(self, treename:str=None):
        savefile = self.treedict[treename].savefile
        print('Savefile for "' + treename + '" :')
        print(savefile)

    @checkname(allowsys=True, replace=True)
    def cd_tree(self, treename:str=None, path:str=None):
        if not path:
            print("Must input path to change directories")
            return False
        if treename==self.SYSCHAR:
            try:
                os.chdir(path)
                return True
            except PermissionError:
                print('Permission denied.')
                return False
            except Exception as error:
                print('Error: ', error)
                return False
        else:
            return self.treedict[treename].cd(path)

    @checkname(allowsys=True, replace=False)
    def chtree(self, treename):
        self.CTREE = treename


    ### Recording entries


    @checkname(allowsys=False, replace=True)
    def recroot(self, 
            treename:str=None,
            localpath:str='.',
            nickname:str=None,
            treepath:str=None,
            use_index:bool=False):
        if use_index:
            try:
                idx = int(localpath)
            except:
                print('Error: index must be an integer.')
                return
            localpath = name_from_os_dir_index(idx)
        self.treedict[treename].recroot(localpath, nickname, treepath)

    @checkname(allowsys=False, replace=True)
    @accept_index
    def rec(self, treename:str=None, objpath:str='.', verbose:bool=False):
        return self.treedict[treename].rec(objpath, verbose=verbose)

    @checkname(allowsys=False, replace=True)
    @accept_index
    def rrec(self, treename:str=None, objpath:str='.', levels:int=0, verbose_levels:int=0):
        return self.treedict[treename].rrec(objpath, levels, global_ignore=self.ignore_names_list, verbose_levels=verbose_levels)

    @checkname(allowsys=False, replace=True)
    def lrec(self, treename:str=None, objpath:str='.', use_index:bool=False, verbose:bool=False):
        if use_index:
            try:
                idx = int(objpath)
            except:
                print('Error: index must be an integer')
                return
            objpath = name_from_os_dir_index(idx)
        return self.treedict[treename].lrec(objpath, verbose=verbose)

    @checkname(allowsys=False, replace=True)
    def remove(self, treename:str=None, objpath:str='.'):
        self.treedict[treename].remove(objpath)


    ### global ignore list
        
    
    def ignorelist_print(self):
        if len(self.ignore_names_list)==0:
            print(' [ none ] ')
            return
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

    def ignorelist_clear(self):
        self.ignore_names_list = []
    
    def ignorelist_add(self, name:str=None):
        if not name:
            print('Ignore List name cannot be empty.')
            return False
        self.ignore_names_list.append(name)
        return True

    @checkname(allowsys=False, replace=True)
    def ignorelist_add_local(self, treename:str=None, name:str=None):
        self.treedict[treename].ignorelist_add(name)
    
    @checkname(allowsys=False, replace=True)
    def ignorelist_print_local(self, treename:str=None):
        self.treedict[treename].ignorelist_print()
    
    @checkname(allowsys=False, replace=True)
    def ignorelist_remove_local(self, treename:str=None, name:str=None, idx:int=None):
        self.treedict[treename].ignorelist_remove(name, idx)


    ### ### ###


    @checkname(allowsys=False, replace=True)
    def set_localpath(self, treename:str=None, root:str=None, path:str=None):
        if not root:
            print('Error: must give a root name.')
            return
        if not path:
            print('Error: localpath must not be empty.')
            return
        self.treedict[treename].root_set_localpath(root, path)

    @checkname(allowsys=False, replace=True)
    def set_os_type(self, treename:str=None, os_type:str=None):
        self.treedict[treename].set_os_type(os_type)
        print('Tree "' + treename + '" has os type set to "' + str(self.treedict[treename].print_os_type()) + '".')

    @checkname(allowsys=True, replace=True)
    def print_os_type(self, treename:str=None):
        if treename==self.SYSCHAR:
            print(os.name)
        else:
            print(self.treedict[treename].print_os_type())

    @checkname(allowsys=False, replace=True)
    @accept_index
    def update(self, treename:str=None, objpath:str='.'):
        self.treedict[treename].update(objpath)

    @checkname(allowsys=False, replace=True)
    def r_update(self,
            treename:str=None,
            objpath:str='.',
            levels:int=0):
        self.treedict[treename].r_update(objpath, levels)

    @checkname(allowsys=False, replace=False)
    def tie(self, treename, Cfile, Dfile, use_index:bool=False):
        """
        Ties together Cfile in the current tree's current directory
        with Dfile in the other tree's current directory.
        """
        if use_index:
            Cfile, _, _ = name_from_dir_index(self.treedict[self.CTREE].CDIR, Cfile)
            Dfile, _, _ = name_from_dir_index(self.treedict[treename].CDIR, Dfile)
            if not Cfile or not Dfile:
                return
        result, Cdict, Ddict = self.tie_header(treename, Cfile, Dfile)
        if result is None:
            # treename not valid
            return
        if result==2:
            print('Error: cannot tie a file to itself.')
            return
        if result==0:
            self.tie_guts(treename, Cdict, Ddict)

    def tie_guts(self, treename, Cdict, Ddict):
        succeeded = tie_files(Cdict, Ddict, session=self.session, quiet=True)
        if succeeded:
            self.treedict[self.CTREE].has_unsaved_changes = True
            self.treedict[treename].has_unsaved_changes = True
            print('-- ' 
                + self.CTREE + '(' + Cdict['root'] + ')> '
                + Cdict['name'] + ' -> '
                + treename + '(' + Ddict['root'] + ')> '
                + Ddict['name']
                )
    
    def tie_header(self, treename:str, Cfile:str, Dfile:str):
        """
        Turns the paths into dicts, for use in tie files.
        Return codes:
          0 - success
          1 - failed to find one of the objects
          2 - attempted to tie a file to itself
        """
        Cdict = self.treedict[self.CTREE].traverse_path(Cfile)
        if not Cdict:
            # traverse_path() already has some failure text,
            # this is printed in addition to it
            print('   (In tree ' + self.CTREE + ')')
            return 1, dict(), dict()
        Ddict = self.treedict[treename].traverse_path(Dfile)
        if not Ddict:
            print('   (In tree ' + treename + ')')
            return 1, dict(), dict()
        if Cdict is Ddict:
            return 2, Cdict, Ddict
        return 0, Cdict, Ddict

    @checkname(allowsys=False, replace=True)
    def a_tie(self, treename, Cdir='.', Ddir='.'):
       """
       Ties together all entries in Cdir and Ddir which share a name.
       """
       if Cdir is None or Ddir is None:
           Cdir = self.treedict[self.CTREE].CDIR
           Ddir = self.treedict[treename].CDIR
       result, Cdict, Ddict =  self.tie_header(treename, Cdir, Ddir)
       if result==1:
           return
       if result==2:
           print('Error: cannot tie a file to itself.')
           return
       if result==0:
           if Cdict['type'] not in DIR_LIST_TYPES or Ddict['type'] not in DIR_LIST_TYPES:
               print('Error: both entries must be directories.')
               return
           all_c_entries = [entry 
                   for entry in Cdict['dir_list']+Cdict['file_list'] 
                   if entry['type']!='unrecorded']
           all_d_entries = [entry 
                   for entry in Ddict['dir_list']+Ddict['file_list'] 
                   if entry['type']!='unrecorded']
           for c_entry in all_c_entries:
               for d_entry in all_d_entries:
                   if c_entry['name']==d_entry['name']:
                       self.tie_guts(treename, c_entry, d_entry)


    @checkname(allowsys=False, replace=True)
    @accept_index
    def add_note(self, treename:str=None, file:str=None, note_text:str=None):
        if not file:
            print("Error: file name required.")
            return
        if not note_text:
            print("Error: note text cannot be empty.")
            return
        self.treedict[treename].add_note(file, note_text)

    @checkname(allowsys=False, replace=True)
    @accept_index
    def remove_note(self, treename:str=None, file:str=None, note_idx:int=None):
        if not file:
            print("Error: file name required.")
            return
        if note_idx is None:
            print("Error: note index required.")
            return
        self.treedict[treename].remove_note(file, note_idx)

    @checkname(allowsys=True, replace=True)
    @accept_index
    def info(self, treename:str=None, filename:str='.', option:str=None, sys_do_hash:bool=False):
        if treename==self.SYSCHAR:
            print_os_file_info(filename, do_hash=sys_do_hash)
        else:
            self.treedict[treename].info(filename, option=option)
    
    @checkname(allowsys=False, replace=True)
    @accept_index
    def history(self, treename:str=None, filename:str='.', full:bool=False):
        self.treedict[treename].history(filename, full)

    @checkname(allowsys=False, replace=True)
    @accept_index
    def notes(self, treename:str=None, filename:str='.'):
        self.treedict[treename].notes(filename)

    @checkname(allowsys=False, replace=True)
    @accept_index
    def ties(self, treename:str=None, filename:str='.'):
        self.treedict[treename].ties(filename)


