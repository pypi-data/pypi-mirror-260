from treerec.primitives import VERSION_NUMBER
from treerec.dirutils import name_from_dir_index
from treerec.engine import TreeEngine
from treerec.commands import *
import os


def retrieve(parameters:dict, key:str, fallback:str=None):
    """
    This command pulls info from the `parameters` (aka `data`) dict that
    all the commands use. Includes default fallback cases.
    """
    out = parameters.get(key, None)
    if type(out) is str:
        return out.strip()
    elif out is None:
        out = fallback
    return out


class TreeObj_Cursor():

    def __init__(self):
        self.engine = TreeEngine()
        self.command_dict = self.build_command_dict()
        self.time_to_leave = False

    def prompt(self, default=False):
        if (self.engine.CTREE is None) or default:
            return "   :> "
        elif self.engine.CTREE==self.engine.SYSCHAR:
            return '  $> '
        else:
            onsystem_indicator = ('o' if self.engine.treedict[self.engine.CTREE].onsystem else ' ')
            active_indicator = ('a' if self.engine.treedict[self.engine.CTREE].is_active() else ' ')
            unsaved_indicator = ('u' if self.engine.treedict[self.engine.CTREE].has_unsaved_changes else ' ')
            return unsaved_indicator + active_indicator + onsystem_indicator + '|' + self.engine.CTREE + ":> "

    def confirm_choice(self, confirmation_prompt):
        print(confirmation_prompt)
        cur_input = input(self.prompt(True))
        madout = ConfirmationInputParser(cur_input)
        return retrieve(madout[1], 'confirm')

    def treelist_nonempty(self, func):
        def wrapper(*args, **kwargs):
            if self.engine.CTREE == None:
                print('No trees in current session.')
                return
            return func(*args, **kwargs)
        return wrapper
    
    def two_option_input(self, first:str, second:str, use_index:bool=False):
        """
        This is for all of the commands where the Tree can be placed before
        the main command's parameter (i.e. ls, cd, rec)
        """
        if second:
            treename = first
            filename = second
        else:
            treename = None
            filename = first
        if use_index:
            filename = self.engine.index_to_name(treename, filename)
            if filename is None:
                return False, False
        return treename, filename

    def mainloop(self, print_welcome:bool=True):
        self.time_to_leave = False
        if print_welcome:
            print(' | treerec v. ' + VERSION_NUMBER)
        while not self.time_to_leave:
            cur_input = input(self.prompt())
            self.execute(cur_input, echo_command=False)

    def execute(self, command_input:str='', echo_command:bool=True):
        if echo_command: print(self.prompt(), command_input)
        madout = MainInputParser(command_input)
        if not madout:
            # print the error message
            print(madout)
        else:
            parameters = madout[1]
            cmd = parameters.get('command', None)
            nextcommand = self.command_dict.get(cmd, False)
            if nextcommand!=False:
                if retrieve(parameters, 'help', False):
                    print_help(cmd)
                else:
                    nextcommand(parameters)
        
    def build_command_dict(self):
        """
        This dictionary connects the command identifiers with the class methods
        which they are meant to invoke.
        """
        return {
            cmd_blank: self.empty_input,
            cmd_quit: self.quit,
            cmd_help: self.empty_input,
            cmd_addtree: self.addtree,
            cmd_create_tree: self.create_tree,
            cmd_set_session_name: self.set_session_name,
            cmd_activate_tree: self.activate_tree,
            cmd_deactivate_tree: self.deactivate_tree,
            cmd_echo: self.echo,
            cmd_list_all_trees: self.list_all_trees,
            cmd_list_tree: self.list_tree,
            cmd_on_system: self.on_system,
            cmd_set_savefile: self.set_savefile,
            cmd_ls: self.ls,
            cmd_cd: self.cd,
            cmd_cdls: self.cdls,
            cmd_recroot: self.recroot,
            cmd_set_localpath: self.set_localpath,
            cmd_rec: self.rec,
            cmd_remove: self.remove,
            cmd_save: self.save,
            cmd_rename: self.rename,
            cmd_droptree: self.droptree,
            cmd_pwt: self.pwt,
            cmd_change_tree: self.chtree,
            cmd_tie: self.tie,
            cmd_info: self.info,
            cmd_history: self.history,
            cmd_print_ties: self.ties,
            cmd_set_hash: self.set_hash,
            cmd_set_os_type: self.set_os_type,
            cmd_pwd: self.pwd,
            cmd_update: self.update,
            cmd_notes: self.note,
            cmd_autoupdate: self.autoupdate,
            cmd_ignore: self.ignore_list
        }

    def empty_input(self, parameters):
        """ 
        For use with the BLANK function, for when the
        user just hits return.
        """
        pass

    def quit(self, parameters):
        result = self.confirm_choice("Are you sure you want to quit? (y/n)")
        if not result:
            return
        if self.engine.has_unsaved():
            result = self.confirm_choice("Tree(s) have unsaved changes! Are you sure? (y/n)")
            if not result:
                return
        print("Goodbye!")
        self.time_to_leave = True

    def echo(self, parameters):
        """
        Mostly, this is a simple test command.
        """
        print(retrieve(parameters, 'text', ''))

    def addtree(self, parameters):
        if retrieve(parameters, 'newtree'):
            self.create_tree(parameters)
        else:
            self.load_tree(parameters)

    def create_tree(self, parameters):
        """
        Creates a new tree.
        A Tree must have a save file, a Device name, and a Nickname.
        For loaded trees, the default Nickname is the Device name.
        """
        if not self.engine.session:
            print('Set session name before creating new trees.')
            return
        filename = retrieve(parameters, 'filename')
        nickname = retrieve(parameters, 'nickname')
        device = retrieve(parameters, 'device')
        if (nickname is None) or (device is None):
            print("Error: Must specify device (-d) and nickname (-n) when creating a new tree.")
        if not nickname:
            print("Error: Nickname cannot be blank.")
            return
        if not device:
            print("Error: Device name cannot be blank.")
            return
        nickstring = (' with nickname "' + nickname + '"' if nickname != None else '')
        print("Creating new tree with save file " + filename + nickstring + ' ...')
        self.engine.new_tree(filename, device, nickname)
        self.on_system( {
            'devname': device,
            'name': nickname,
            'action': 'on'
            } )
        self.activate_tree({
            'name': nickname
            } )

    def load_tree(self, parameters):
        """
        Load a tree from the savefile.
        """
        nickname = retrieve(parameters, 'nickname')
        filename = retrieve(parameters, 'filename')
        nickstring = (' with nickname "' + nickname + '"' if nickname != None else '')
        successValue = self.engine.load_tree(filename, nickname)
        if successValue:
            print("Added tree from file " + filename + nickstring + ' ...')

    def set_session_name(self, parameters):
        """
        Sets the Session name for the Multitree.
        """
        name = retrieve(parameters, 'text')
        if name=='':
            print('Cannot have empty Session name.')
            return
        if name is None:
            print('Session: "' + (self.engine.session if self.engine.session else '<None>') + '"')
            return
        self.engine.set_session_name(name)
        print('Setting session name to "' + name + '".')

    def activate_tree(self, parameters):
        name = retrieve(parameters, 'name')
        self.engine.activate(name)

    def deactivate_tree(self, parameters):
        name = retrieve(parameters, 'name')
        self.engine.deactivate(name)

    def rename(self, parameters):
        """
        Changes the Nickname of the Tree in the Cursor.
        We expect the parameters to have values for 'name1' and 'name2'.
        If 'name2'==None, then 'name1' is the new name for the current Tree.
        If 'name2' is not None, then name2 is the new name for the Tree with
          nickname name1.
        """
        if retrieve(parameters, 'name2'):
            target = retrieve(parameters, 'name1')
            newname = retrieve(parameters, 'name2')
        else:
            target = None
            newname = retrieve(parameters, 'name1')
        self.engine.rename(target, newname)


    def list_tree(self, parameters):
        self.engine.print_tree(retrieve(parameters, 'text'))
        print()

    def list_all_trees(self, parameters):
        self.engine.list_trees()
        print()

    def on_system(self, parameters):
        """
        Implements the TreeEngine.set_onsystem(name, device=None) method.
        Device can be set if the Tree is new (i.e. has _no_ children) and
        the device name has not been set yet.
        """
        devname = retrieve(parameters, 'device')
        name = retrieve(parameters, 'name')
        action = retrieve(parameters, 'action')
        if action=='on':
            self.engine.set_onsystem(name, devname)
        elif action=='off':
            self.engine.set_offsystem(name)
        else:
            print('Error: set_on_system action not recognized. Must be either "on" or "off".')

    def set_savefile(self, parameters):
        if retrieve(parameters, 'show'):
            self.engine.print_savefile(retrieve(parameters, 'name1'))
            return
        if retrieve(parameters, 'name2'):
            treename = retrieve(parameters, 'name1')
            filename = retrieve(parameters, 'name2')
        elif retrieve(parameters, 'name1'):
            treename = None
            filename = retrieve(parameters, 'name1')
        else:
            self.engine.print_savefile(None)
            return
        self.engine.set_savefile(
            treename,
            filename,
            force=retrieve(parameters, 'force')
            )

    def ls(self, parameters):
        # first = retrieve(parameters, 'first')
        # second = retrieve(parameters, 'second')
        # use_index = retrieve(parameters, 'index')
        # recorded_only = retrieve(parameters, 'recorded_only')
        # show_mtime = retrieve(parameters, 'mtime')
        treename, dirname = self.two_option_input(
            retrieve(parameters, 'first'),
            retrieve(parameters, 'second'),
            retrieve(parameters, 'index')
            )
        if treename is False:
            return
        self.engine.ls_tree(
            treename, 
            dirname, 
            retrieve(parameters, 'recorded_only'), 
            retrieve(parameters, 'mtime'),
            retrieve(parameters, 'show_index')
            )

    def cd(self, parameters):
        use_index = retrieve(parameters, 'index')
        first = retrieve(parameters, 'first')
        second = retrieve(parameters, 'second')
        if second:
            treename = first
            dirname = second
        else:
            treename = None
            dirname = first
        if use_index:
            dirname = self.engine.index_to_name(treename, dirname)
        if dirname is None:
            return
        self.engine.cd_tree(treename, dirname)
    
    def cdls(self, parameters):
        """cdls: cd, then ls."""
        treename, dirname = self.two_option_input(
            retrieve(parameters, 'input1'),
            retrieve(parameters, 'input2'),
            retrieve(parameters, 'index')
        )
        if treename is False:
            return
        cd_success = self.engine.cd_tree(treename, dirname)
        if cd_success: self.engine.ls_tree(treename, '.')

    def recroot(self, parameters):
        self.engine.recroot(
            None,  # only works on current Tree
            retrieve(parameters, 'localpath'),
            retrieve(parameters, 'name'),
            retrieve(parameters, 'treepath'),
            retrieve(parameters, 'index')
        )

    def set_localpath(self, parameters):
        self.engine.set_localpath(None,
                                  retrieve(parameters, 'root'),
                                  retrieve(parameters, 'path') )

    def rec(self, parameters):
        """Record entries"""
        use_index = retrieve(parameters, 'index')
        use_localpath = retrieve(parameters, 'use_localpath')
        recursive = retrieve(parameters, 'recursive')
        path = retrieve(parameters, 'path')
        verbose = retrieve(parameters, 'verbose')
        try:
            verbose = int(verbose)
        except:
            print('Error: verbose levels must be an integer.')
            return
        try:
            levels = int(retrieve(parameters, 'r_levels'))
        except:
            print('Error with rec -r: recursion level must be an integer greater or equal to 0.')
            return
        if use_localpath and recursive:
            print('Cannot perform recursive record from local path. Use tree path instead.')
            return
        if use_localpath:
            rec_success = self.engine.lrec(None, path, use_index, verbose=bool(verbose))
        elif recursive:
            rec_success = self.engine.rrec(None, path, use_index, levels=levels, verbose_levels=verbose)
        else:
            rec_success = self.engine.rec(None, path, use_index, verbose=bool(verbose))
        if not rec_success:
            return
        if retrieve(parameters, 'cdls'):
            cd_success = self.engine.cd_tree(None, path)
            if cd_success: self.engine.ls_tree(None, '.')
        elif retrieve(parameters, 'cd'):
            self.engine.cd_tree(None, path)

    def remove(self, parameters):
        path = retrieve(parameters, 'path')
        use_index = retrieve(parameters, 'index')
        if use_index:
            try:
                idx = int(path)
            except:
                print('Error: index must be an integer.')
                return
            path, _, _ = name_from_dir_index(self.engine.treedict[self.engine.CTREE].CDIR, idx)
        if not retrieve(parameters, 'confirm'):
            prompt = 'Are you sure you would like to remove:\n' + path + '\nfrom the current Tree?'
            result = self.confirm_choice(prompt)
        else:
            result = True
        if not result:
            return
        self.engine.remove(None, path)

    def save(self, parameters):
        force = retrieve(parameters, 'force', False)
        pretty = retrieve(parameters, 'pretty', False)
        save_all = retrieve(parameters, 'all')
        if save_all:
            self.engine.saveall(force=force, pretty=pretty)
        else:
            treename = retrieve(parameters, 'tree')
            self.engine.save(treename, force=force, pretty=pretty)

    def droptree(self, parameters):
        self.engine.droptree(
            retrieve(parameters, 'tree'),
            retrieve(parameters, 'force')
        )

    def pwt(self, parameters):
        self.engine.pwt()

    def chtree(self, parameters):
        self.engine.chtree(retrieve(parameters, 'tree'))

    def tie(self, parameters):
        index = retrieve(parameters, 'index')
        # index_num = retrieve(parameters, 'indexNum')
        treename = retrieve(parameters, 'tree')
        source = retrieve(parameters, 'source')
        destination = retrieve(parameters, 'destination')
        # use_Cindex = False
        # use_Dindex = False
        # if index:
            # use_Cindex = use_Dindex = True
        if retrieve(parameters, 'all'):
            self.engine.a_tie(treename)
        else:
            self.engine.tie(treename, source, destination, index)

    def info(self, parameters):
        treename, filename = self.two_option_input(
            retrieve(parameters, 'input1'),
            retrieve(parameters, 'input2'),
            retrieve(parameters, 'index')
        )
        if retrieve(parameters, 'history'):
            if retrieve(parameters, 'ties'):
                print('Cannot use both --history and --ties flag when using info.')
                return
            self.engine.history(
                    treename,
                    filename,
                    False,
                    retrieve(parameters, 'full')
                    )
        elif retrieve(parameters, 'ties'):
            self.engine.ties(
                    treename,
                    filename,
                    False
                    )
        else:
            self.engine.info(
                treename, 
                filename, 
                False,
                retrieve(parameters, 'amount'), 
                retrieve(parameters, 'sys_hash')
                )
    
    def history(self, parameters):
        self.info( {
            'index': retrieve(parameters, 'index'),
            'history': True,
            'ties': False,
            'input1': retrieve(parameters, 'input1'),
            'input2': retrieve(parameters, 'input2'),
            'full': retrieve(parameters, 'full')
            } )

    def ties(self, parameters):
        self.info( {
            'index': retrieve(parameters, 'index'),
            'history': False,
            'ties': True,
            'input1': retrieve(parameters, 'input1'),
            'input2': retrieve(parameters, 'input2')
            } )
    
    def set_hash(self, parameters):
        affirmative = ['y', 'yes', 'on', 'do']
        negative = ['n', 'no', 'off', 'dont']
        action = str.lower(retrieve(parameters, 'action'))
        treename = self.engine.CTREE
        if action in affirmative:
            self.engine.set_hash_rule(treename, True)
            print('"' + treename + '" will now hash recorded files.')
        elif action in negative:
            self.engine.set_hash_rule(treename, False)
            print('"' + treename + '" will no longer hash recorded files.')
        else:
            print('Unrecognized action: "' + action + '". Choose "on" or "off".')
        
    def set_os_type(self, parameters):
        if retrieve(parameters, 'reset'):
            self.engine.set_os_type(
                    retrieve(parameters, 'input1'),
                    None)
            return
        if retrieve(parameters, 'show'):
            self.engine.print_os_type(
                    retrieve(parameters, 'input1', None))
            return
        if retrieve(parameters, 'input2'):
            treename = retrieve(parameters, 'input1')
            osname = retrieve(parameters, 'input2')
        elif retrieve(parameters, 'input1'):
            treename = None
            osname = retrieve(parameters, 'input1')
        else:
            self.engine.print_os_type()
            return
        self.engine.set_os_type(treename, osname)

    def pwd(self, parameters):
        style = ('tree' if retrieve(parameters, 'full') else
                ('local' if retrieve(parameters, 'local') else False))
        self.engine.pwd(
                retrieve(parameters, 'tree'),
                style)

    def update(self, parameters):
        """
        Update files of current Tree.
        -r : recursive update
        -a : all entries in directory, and directory itself
        -RR: all entries in all children, recursively
        """
        path = retrieve(parameters, 'path')
        use_index = retrieve(parameters, 'index')
        if retrieve(parameters, 'all'):
            self.engine.r_update(None, path, 0)
        elif retrieve(parameters, 'recursive'):
            # both -r and -RR fall into this category.
            self.engine.r_update(None, path, retrieve(parameters, 'r_levels'))
        else:
            self.engine.update(None, path, use_index)

    def note(self, parameters):
        action = retrieve(parameters, 'action')
        use_index = retrieve(parameters, 'index')
        if action=='show':
            treename, filename = self.two_option_input(
                retrieve(parameters, 'input1'),
                retrieve(parameters, 'input2'),
                retrieve(parameters, 'index')
            )
            if treename is False:
                return
            self.engine.notes(treename, filename, False)
            return
        elif action=='add':
            filename = retrieve(parameters, 'input1')
            note_text = retrieve(parameters, 'input2')
            self.engine.add_note(None, filename, use_index, note_text)
        elif action=='remove':
            filename = retrieve(parameters, 'input1')
            user_idx = retrieve(parameters, 'input2')
            try:
                idx = int(user_idx)
            except:
                print("Error: note index must be an integer.")
                print("Usage: note -r [FILE] [INDEX]")
                print('Index corresponds to "Note X" when using `note [FILE]`.')
                return
            self.engine.remove_note(None, filename, use_index, idx)
        else:
            print('Unrecognized action.')
            return

    def autoupdate(self, parameters):
        if retrieve(parameters, 'show'):
            treename = retrieve(parameters, 'input1')
            self.engine.show_auto_update(treename)
            return
        if retrieve(parameters, 'input2'):
            treename = retrieve(parameters, 'input1')
            action = retrieve(parameters, 'input2')
        elif retrieve(parameters, 'input1'):
            treename = None
            action = retrieve(parameters, 'input1')
        else:
            self.engine.show_auto_update(None)
            return
        if str.lower(action) in ['on', 'true', '1', 'yes']:
            self.engine.set_auto_update(treename, True)
        elif str.lower(action) in ['off', 'false', '0', 'no']:
            self.engine.set_auto_update(treename, False)
        else:
            print('Error: unrecognized action ("on" / "off").')
            return

    def ignore_list(self, parameters):
        input = retrieve(parameters, 'input')
        remove = retrieve(parameters, 'remove')
        use_index = retrieve(parameters, 'index')
        clear_entries = retrieve(parameters, 'clear')
        if clear_entries:
            self.engine.ignorelist_clear()
            return
        if remove and use_index:
            try:
                idx = int(input)
                self.engine.ignorelist_remove(None, idx)
                ## Add helptext to `ignore`; add -i to adding names in current directory to ignorelist
                return
            except:
                print('Error: when using -r -i, you must use an integer index.')
                return
        if remove:
            self.engine.ignorelist_remove(input, None)
            return
        if input:
            self.engine.ignorelist_add(input)
            return
        self.engine.ignorelist_print()
        return

##############
##############


def print_help(cmd):
    helptext = ''
    if cmd==cmd_help:
        helptext = (
            'treerec: a Python package for recording directory tree / file information.',
            '   https://github.com/JWMerritt/treerec',
            '',
            'Common commands:',
            'Type `cmd -h` to see help for any command',
            '',
            'quit              Quit the application.',
            'ls PATH           List contents of directory PATH.',
            'cd PATH           Change directory to PATH.',
            'cdls PATH         Change directory and list contents.',
            'chtree TREE       Change the current working Tree.',
            '                    "$" represents the System.',
            'tree              Display info about the current Tree.',
            'trees             Display info about all currently loaded Trees.',
            'load PATH         Load the json file at PATH as a Tree.',
            'create NAME DEVICE PATH',
            '                  Create new Tree NAME with Device name DEVICE, with a',
            '                    save file at PATH.',
            'os TYPE           Changes recorded OS type to TYPE. Usually, should be',
            '                    either "posix" or "nt". This is here because',
            '                    st_ctime means something different for',
            '                    posix or nt systems.',
            'savefile PATH     Sets the save file of the current Tree.',
            'session SESSION   Set the name for the current Session.',
            '                    Generally, the Session name is recorded along',
            '                    with any actions taken on the Tree.',
            'onsystem          Declare that the current tree is on-system.',
            '                    This means that the Tree paths mirror the',
            '                    actual locations on the current System.',
            'activate          Activate the current Tree. Changes cannot',
            '                    be made to a Tree unless it is active.'
            'autoupdate ON/OFF ',
            '                  Turn on/off automatically updating the',
            '                    unrecorded entries of directories in',
            '                    the current Tree (only effective if',
            '                    Tree is on-system).',
            'sethash ON/OFF    Turn on/off hashing of files when they are',
            '                    recorded on current Tree.',
            'recroot PATH      Record the System directory at the system PATH',
            '                    as a Tree Root.',
            'local ROOT PATH   Set the local (System) path of ROOT to PATH.',
            'rec PATH          Record the file at the Tree PATH into the current Tree.',
            'rec -a            Record all entries in current Tree directory.',
            'rec -r NUM        Recursively record entries for NUM levels.',
            '                    `rec -r 1 .` is identical to `rec -a`.',
            'rec -RR           Record all descendants of PATH.',
            'ignore NAME       Add name to the Ignore List.',
            'remove FILE       Removes recorded file or directory (and all children!)',
            '                    from the current Tree.',
            'info FILE         Prints information about a file or directory.',
            'history FILE      Print the history of a file or directory.',
            'note FILE         Add or read notes attached to a file or directory.',
            'tie FILE_A TREE FILE_B',
            '                  Tie FILE_A in the current Tree to FILE_B in the',
            '                    destination Tree TREE. Tied files are meant to',
            '                    indicate that these are the same file,',
            '                    saved in two different locations.'
        )

    elif cmd==cmd_quit:
        helptext = ('You should not be seeing this text...','')

    elif cmd==cmd_echo:
        helptext = ('Usage: echo [TEXT (optional)]',
                   'Print text to the terminal. Text must be surrounded in double quotes ( " " ) if it includes spaces.')

    elif cmd==cmd_addtree:
        helptext = (
            'Usage: load [OPTIONS] [SAVEFILE]',
            '  AKA: add, addtree',
            'Add a Tree to the current Session, loaded from SAVEFILE.',
            '',
            '-n  --nickname  Set the local nickname for the tree, which is used when',
            '                  referencing the tree in commands. It defaults to the device name.',
            '-c  --create    Create a new tree. It will be saved in SAVEFILE.',
            '                  It is recommended to use the `create` command instead.',
            '-d  --device    Set the device name. Only used when creating a new tree.'
        )

    elif cmd==cmd_set_session_name:
        helptext = (
            'Usage: session [NAME (optional)]',
            'Set the Name of the current Session. This will be recorded along with any updates to any Trees.',
            'If no parameters are given, prints the name of the current session.'
        )

    elif cmd==cmd_activate_tree:
        helptext = (
            'Usage: activate [TREE (optional)]',
            'Activate TREE (current Tree by default).',
            'Active Trees can be modified (record files, add notes, etc.).'
        )

    elif cmd==cmd_deactivate_tree:
        helptext = (
            'Usage: deactivate [TREE (optional)]',
            'Deactivate TREE (current Tree by default).'
        )

    elif cmd==cmd_rename:
        helptext = (
            'Usage: rename [TREE (optional)] [NICKNAME]',
            '  AKA: name',
            'Change the Nickname of TREE (defaults to current tree) to NICKNAME'
            )

    elif cmd==cmd_list_tree:
        helptext = (
            'Usage: tree [TREE (optional)]',
            '  AKA: lstree',
            'List details about TREE (defaults to current Tree).'
        )

    elif cmd==cmd_list_all_trees:
        helptext = (
            'Usage: trees'
            '  AKA: list, lstrees',
            'Lists all currently loaded Trees by Nickname.'
        )

    elif cmd==cmd_on_system:
        helptext = (
            'Usage: onsystem [OPTIONS] [TREE (optional)] [ACTION = "on"/"off" (optional)]'
            '  AKA: on, on_system',
            'Sets the TREE (defaults to current Tree) on-system property (defaults to "on").',
            'A Tree that is on-system means that it is on its native hardware,',
            'its paths mirror actual System paths, and files can be recorded to it.',
            '',
            '`onsystem TREE off` is identical to `offsystem TREE`.',
            '',
            '-d  --device [NAME]  Sets the name of the device. Only if the Tree is new',
            '                       and the device name has not yet been set.'
        )

    elif cmd==cmd_set_savefile:
        helptext = (
            'Usage: savefile [OPTIONS] [TREE (optional)] [FILE]',
            '  AKA: setsave, set_savefile',
            'Sets the save file of TREE (defaults to current Tree) to be FILE.',
            'If no parameters are entered, displays the save file of the current Tree.',
            '',
            '-s  --show [TREE]  Show the savefile for TREE. Defaults to current tree.',
            '-f  --force        Force the save file. Otherwise, command fails if the save file',
            '                     already exists.'
        )

    elif cmd==cmd_cd:
        helptext = (
            'Usage: cd [OPTIONS] [TREE (optional)] [DIR]',
            'Change the directory to DIR in TREE (defaults to current Tree).',
            '"$" represents the current system.',
            '',
            '-i  --index       Select directory by index instead of name.'
            )
    
    elif cmd==cmd_ls:
        helptext = (
            'Usage: ls [OPTIONS] [TREE (optional)] [DIR (optional)]',
            '  AKA: dir',
            'List the contents of DIR (defaults to current directory) in TREE (defaults to current tree).',
            '"$" represents the current system.',
            'Remember that the directory path is required if the Tree name is entered',
            '  (i.e. `ls` and `ls .` list the contents of the current directory, and',
            '  `ls $ .` list the contents of the system''s current directory, but',
            '  `ls $` just returns an error).',
            '',
            '-i  --index      Select directory by index instead of name.',
            '-I               Print entry indices.',
            '-r  --recorded   List only the recorded entries of the directory.',
            '-m               Print mtime (time last modified) after file names.'
        )

    elif cmd==cmd_cdls:
        helptext = (
            'Usage: cdls [TREE (optional)] [FILE]',
            'Change directory, and then list contents of directory.',
            'Exactly the same as `cd [FILE]; ls`',
            '',
            '-i  --index         Select directory by index instead of name.'
        )
    
    elif cmd==cmd_recroot:
        helptext = (
            'Usage: recroot [OPTIONS] [PATH]',
            '  AKA: newroot',
            'Record system file at local (System) PATH as a Root of the current tree.',
            '',
            '-i  --index                    Select directory by index instead of name.',
            '                                 Note that this corresponds to the *System*',
            '                                 index for the directory.',
            '-n  --name  --nickname [NAME]  Give the Root a nickname.',
            '-p  --path  --treepath [PATH]  Give the Root a (tree) path.',
            '                                 The folder and all of its recorded descendants',
            '                                 will have their paths reflect this root path.'
        )
    
    elif cmd==cmd_rec:
        helptext = (
            'Usage: rec [OPTIONS] [PATH]',
            'Record system object located at PATH. Uses Tree-path by default.',
            '',
            '-i  --index                Select entry by index instead of name.',
            '-l  --local  --localpath   Record file using local (device) path instead of tree-path.',
            '-a  --all                  Record all entries in the current directory.',
            '-r  --recursive [LEVELS]   Record recursively for LEVELS levels.',
            '                             `rec -r 0 [PATH]` is identical to `rec [PATH]`.',
            '                             `rec -r 1` records all entries in PATH,',
            '                             identical to `rec -a` if PATH is current directory.',
            '-RR                        Record all entries in all children of current directory.',
            '                             Effectively equal to `rec -r infinity`.'
            '-v  --verbose              Print the name of each entry as it is recorded.',
            '                             Prints ">>>" when entering directory to record its children.',
            '-vv  --verbose-levels [LEVELS]',
            '                           Only print the name of recorded entries to a number of LEVELS.',
            '-cd                        Change into the new directory after recording',
            '-cdls                      Change into newly recorded directory, and list contents.'
        )
    
    elif cmd==cmd_save:
        helptext = (
            'Usage: save [OPTIONS] [TREE (optional)]',
            'Save TREE (defaults to the current tree) to its savefile.',
            '',
            '-a  --all     Saves all active and unsaved trees.',
            '-f  --force   Forces an unsaved tree to save, even if it is not active.',
            '-p  --pretty  Saves json file with indentations, for readability.',
            '                should only be used for debugging/testing, as this can',
            '                triple the size of a savefile.'
            )

    elif cmd==cmd_droptree:
        helptext = (
            'Usage: drop [TREE]',
            '  AKA: droptree',
            'Remove TREE from the current session. Does NOT default to the current tree.',
            '',
            '-f  --force  Forcefully remove tree, even if it has unsaved changes.'
        )
            
    elif cmd==cmd_pwt:
        helptext = (
            'Usage: pwt',
            'A redundant command to print the name of the present working tree.',
            'M.pwt() is more useful in a Python interpreter setting, where M = treerec.TreeEngine().'
        )

    elif cmd==cmd_change_tree:
        helptext = (
            'Usage: chtree [TREE]',
            '  AKA: cdtree, cht, cdt',
            'Change the current working Tree.'
            )
    
    elif cmd==cmd_tie:
        helptext = (
            'Usage: tie [FILE A] [TREE] [FILE B]',
            'Ties together FILE A in the current Tree and FILE B in TREE.',
            'FILE B is a path in TREE. ".", "..", "^", and "^^" are relative to TREE''s current directory.',
            'Tying files creates a new Tie entry, which records the name and location of its tied file.',
            'This is meant to show that the files are the same, just copied across different devices.',
            '',
            '-i  --index          Select entries by indices instead of names. Applies to files in both Trees.',
            '-a  --all TREE       Tie together all entries inside of the *current directory*',
            '                       with files of the same name in the *current directory* of TREE.'
        )
    
    elif cmd==cmd_info:
        helptext = (
            'Usage: info [TREE (optional)] [FILE]',
            'Print the info for FILE in TREE (defaults to current Tree).',
            '',
            '-i  --index    Select entry by index instead of name.',
            '-l  --long     Print an expanded version of the information.',
            '-H  --do-hash  (For System files) calculate SHA256 hash for file.'
        )

    elif cmd==cmd_set_hash:
        helptext = (
            'Usage: sethash  [ACTION = "on"/"off"]',
            '  AKA: hash',
            'Set the hash rule for the current tree. By default, Trees calculate the SHA256',
            '  hash of the files they record.'
        )
    
    elif cmd==cmd_set_localpath:
        helptext = (
            'Usage: localpath [ROOT] [PATH]',
            '  AKA: local, set_localpath',
            'Sets the local (System) path of the Root.',
            'This is especially important for an archive drive, which will be at',
            '  different mount points when plugged into different systems.'
        )

    elif cmd==cmd_set_os_type:
        helptext = (
            'Usage: set_os [TREE (optional)] [OS_TYPE]',
            '  AKA: os, setos',
            'Sets the OS type for recorded entries on TREE (defaults to current tree).',
            'The OS type is only important because the interpretation of a file C-time',
            '  (st_ctime) is different on nt and posix systems.',
            'Generally, OS_TYPE should be either "nt" or "posix".',
            '',
            'If no parameters, are entered, displays the current OS type for current Tree (or Ssytem).',
            '',
            '-r     Resets os type (uses os of host system).'
            )

    elif cmd==cmd_pwd:
        helptext = (
            'Usage: pwd [TREE (optional)]',
            'Pring Working Directory of TREE (defaults to current Tree).',
            '',
            '-f  --full    Print full tree path',
            '-l  --local   Print full local path'
            )

    elif cmd==cmd_update:
        helptext = (
            'Usage: update [ENTRY]',
            'Updates ENTRY in the current Tree to match that on the System.',
            'For directories, this adds new unrecorded entries which are present',
            '  on the System, and removes unrecorded entries which are not',
            '  present on the system.',
            '',
            '-i  --index               Select by index indstead of name.',
            '-a  --all                 Update [ENTRY] (a directory) and all entries inside it.',
            '-r  --recursive [LEVELS]  Recurive update: update ENTRY and all children,',
            '                            up to LEVELS levels.',
            '-RR                       Recursive update current directory, and all',
            '                            children to all levels'
            )

    elif cmd==cmd_notes:
        helptext = (
            'Usage: note [TREE (optional)] [FILE]',
            'Printing and manipulation of attached Notes.',
            'By default, prints all notes attached to FILE from Tree TREE (defaults',
            '  to current Tree).',
            '',
            '-i  --index               Select by index instead of name.',
            '-a  --add [FILE] [TEXT]   Add new note to the file (in current Tree).',
            '                            It is *highly* encouraged that text is',
            '                            wrapped in double-quotes (though this ',
            '                            isn''t strictly necessary).',
            '-r  --remove [IDX]        Remove note with index IDX. Note index is printed as',
            '                            ">> Note IDX" when using note [FILE].'
            )

    elif cmd==cmd_history:
        helptext = (
            'Usage: history [TREE (optional)] [FILE]',
            '  AKA: hist',
            'Print the history of FILE (file or directory) in TREE (defaults',
            '  to current Tree).',
            '',
            '-i --index  Select entry by index instead of name.',
            '-f --full   Show more detailed information.'
            )

    elif cmd==cmd_print_ties:
        helptext = (
            'Usage: ties [TREE (optional)] [FILE]',
            'Print info about all of the files tied to FILE in TREE (defaults to current Tree).',
            ''
            'Format:',
            '1|  >> File  <Device Name>',
            '2|   C:/Program Files/Company/File',
            '3|   (Root)/File',
            '4|   Session: session name',
            '5|   Time: 12/Feb/20xx',
            '',
            '  1 - Name of tied file, and the device that it is on.',
            '        This line will have a " * " in front if the two files',
            '        had identical hashes at the time they were tied.',
            '  2 - The full Tree Path of the tied file.',
            '  3 - The Root (Tree) Path of the tied file, using the Root nickname.',
            '  4 - The name of the Session during which these two files were tied.',
            '  5 - The time at which the two files were tied.',
            '',
            '-i  --index     Select entry by index instead of name.'
            )

    elif cmd==cmd_autoupdate:
        helptext = (
            'Usage: autoupdate [TREE (optional)] [ACTION = "on"/"off"]',
            '  AKA: auto_update',
            'Sets the autoupdate property of TREE (defaults to current Tree) to be ACTION.',
            '',
            '-s  --show [TREE]  Shows current autoupdate setting for TREE',
            '                     (defaults to the current Tree).'
            )

    elif cmd==cmd_ignore:
        helptext = (
            'Usage: ignore [OPTIONS] [NAME]',
            '  AKA: ignorelist',
            'Adds name to the Ignore List, a list of file/directory names which are',
            '  ignored when recording multiple entries (i.e. `rec -a, -r, -RR`).',
            'If no parameters are entered, prints contents of Ignore List.',
            '',
            '-r  --remove        Remove a name from the Ignore List.',
            '-i  --index         Remove a name from the Ignore List by index.',
            '-c  --clear         Clear the Ignore List.'
        )

    print('\n'.join(helptext) + '\n')
 

##########
##########


if __name__=="__main__":
    os.chdir('..')
    print(os.getcwd())
    print(os.listdir())
    O = TreeObj_Cursor()
    O.mainloop()
