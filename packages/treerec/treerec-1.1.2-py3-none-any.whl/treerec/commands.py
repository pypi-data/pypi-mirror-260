from treerec.command_parser import *
from copy import copy


helpflags = ('-h', '--help', '--h', '-help')


cmd_blank = 'blank'
cmd_quit = 'quit'
cmd_help = 'help'
cmd_addtree = 'addtree'
cmd_create_tree = 'createtree'
cmd_set_session_name = 'sessionname'
cmd_activate_tree = 'activate_tree'
cmd_deactivate_tree = 'deactivate_tree'
cmd_echo = 'echo'
cmd_list_all_trees = 'list_trees'
cmd_list_tree = 'list_tree'
cmd_on_system = 'on_system'
cmd_set_savefile = 'set_savefile'
cmd_ls = 'ls'
cmd_cd = 'cd'
cmd_cdls = 'cdls'
cmd_recroot = 'recroot'
cmd_set_localpath = 'root_localpath'
cmd_rec = 'rec'
cmd_remove = 'remove'
cmd_save = 'save'
cmd_rename = 'rename'
cmd_droptree = 'droptree'
cmd_pwt = 'pwt'
cmd_change_tree = 'chtree'
cmd_tie = 'tie'
cmd_info = 'info'
cmd_history = 'history'
cmd_print_ties = 'ties'
cmd_set_hash = 'sethash'
cmd_set_os_type = 'set_os_type'
cmd_pwd = 'pwd'
cmd_update = 'update'
cmd_notes = 'note'
cmd_remove_note = 'remove_note'
cmd_autoupdate = 'auto_update'
cmd_ignore = 'ignore_list'
## Include rec -a flags for recording only files / directories
##      -> update command_parser to include an InputParam that takes an
##          arbitrary number of inputs
## Include a ls flag (-o <var>) for sorting outputs
##
## Add helptext to `ignore`; add -i to adding names in current directory to ignorelist


BLANK = CommandInput(
    '', ' ', '\t', '\n', '\r', '\r\n', '\n\r', '\r\r', '\n\n',
    default_data=blank_dict(cmd_blank),
    final=True,
    terminal=True
)


QUIT = CommandInput(
    'quit', 'exit', 'q', 'bye', 'goodbye',
    include_help=True,
    final=True,
    terminal=True,
    action_func=mykey_func('command', cmd_quit),
)


ECHO = CommandInput(
    'echo',
    include_help=True,
    default_data={
        'command': cmd_echo,
        'text': None,
    },
    children=[
        OptionalVariableInputParam(
            final=True,
            terminal=True,
            action_func=theirkey_func('text')
        )
    ]
)


CMD_HELP = CommandInput(
    'help', 'h',
    include_help=False,
    default_data={
        'command': cmd_help,
        'help': True
    },
    terminal=True
)


SET_SESSION_NAME = CommandInput(
    'sessionname', 'session',
    include_help=True,
    default_data= {
        'command': cmd_set_session_name,
        'text' : None,
    },
    children=[
        OptionalVariableInputParam(
            final=True,
            terminal=True,
            action_func=theirkey_func('text')
        )
    ]
)

LIST_ALL_TREES = CommandInput(
    'lstrees', 'trees', 'list',
    include_help=True,
    default_data=blank_dict(cmd_list_all_trees),
    terminal=True  # command_parser is set to still accept flags, even if a command is terminal
)


LIST_TREE = CommandInput(
    'lstree', 'tree',
    include_help=True,
    default_data=blank_dict(cmd_list_tree, 'text'),
    children=[
        OptionalVariableInputParam(
            terminal=True,
            action_func=theirkey_func('text')
        )
    ]
)


ADD_TREE = CommandInput(
    'addtree', 'add_tree', 'add', 'load',
    include_help=True,
    default_data={
        'command': cmd_addtree,
        'filename': None,
        'nickname': None,
        'newtree': False,
        'device': None
    },
    flags=[
        InputParam(
            '-c', '--new', '--create',
            final=True,
            action_func=mykey_func('newtree', True)
        ),
        InputParam(
            '-d', '--dev', '-dev', '--device',
            final=False,
            action_func=blank_func(),
            children=[
                VariableInputParam(
                    final=True,
                    terminal=False,
                    action_func=theirkey_func('device')
                )
            ]
        ),
        InputParam(
            '-n', '--name', '--nickname',
            final=False,
            action_func=blank_func(),
            children=[
                VariableInputParam(
                    final=True,
                    terminal=False,
                    action_func=theirkey_func('nickname')
                )
            ]
        )
    ],
    children=[
        VariableInputParam(
            final=True,
            terminal=True,
            action_func=theirkey_func('filename'),
        )
    ]
)


CREATE_TREE = CommandInput(
        'create', 'new',
        include_help=True,
        default_data={
            'command': cmd_create_tree,
            'nickname': None,
            'device': None,
            'filename': None
            },
        children=[
            VariableInputParam(
                action_func=theirkey_func('nickname'),
                children=[
                    VariableInputParam(
                        action_func=theirkey_func('device'),
                        children=[
                            VariableInputParam(
                                action_func=theirkey_func('filename'),
                                terminal=True
                                )
                            ]
                        )
                    ]
                )
            ]
        )


RENAME_TREE = CommandInput(
    'rename', 'name',
    include_help=True,
    default_data = {
        'command': cmd_rename,
        'name1': None,
        'name2': None
    },
    children = [
        VariableInputParam(
            action_func=theirkey_func('name1'),
            children=[
                OptionalVariableInputParam(
                    terminal=True,
                    action_func=theirkey_func('name2')
                )
            ]
        )
    ]
)


ACTIVATE_TREE = CommandInput(
    'activate', 'active',
    include_help=True,
    default_data={
        'command': cmd_activate_tree,
        'name': None,
        'session': None
    },
    children=[
        OptionalVariableInputParam(
            action_func=theirkey_func('name'),
            children=[
                OptionalVariableInputParam(
                    final=True,
                    terminal=True,
                    action_func=theirkey_func('session')
                )
            ]
        )
    ]
)


DEACTIVATE_TREE = CommandInput(
    'deactivate', 'inactive',
    include_help=True,
    default_data={
        'command': cmd_deactivate_tree,
        'name': None
    },
    children=[
        OptionalVariableInputParam(
            action_func=theirkey_func('name'),
            final=True,
            terminal=True
        )
    ]
)


ON_SYSTEM = CommandInput(
    'onsystem', 'on_system', 'on',
    include_help=True,
    default_data={'command': cmd_on_system,
                  'name': None,
                  'action': 'on',
                  'device': None},
    flags=[
        InputParam(
            '-d', '--device',
            action_func=blank_func(),
            children=[
                VariableInputParam(
                    final=True,
                    terminal=False,
                    action_func=theirkey_func('device')
                )
            ]
        )
    ],
    children=[
        OptionalVariableInputParam(
            action_func=theirkey_func('name'),
            children=[
                OptionalVariableInputParam(
                    final=True,
                    terminal=True,
                    action_func=theirkey_func('action')
                )
            ]
        )
    ]
)

OFF_SYSTEM = CommandInput(
    'offsystem', 'off_system', 'off',
    include_help=True,
    default_data={'command': cmd_on_system, 'name': None, 'action': 'off'},
    children=[
        OptionalVariableInputParam(
            final=True,
            terminal=True,
            action_func=theirkey_func('name')
        )
    ]
)

SET_SAVE_FILE = CommandInput(
    'setsave', 'savefile', 'set_savefile',
    include_help=True,
    default_data={
        'command': cmd_set_savefile,
        'name1': None,
        'name2': None,
        'force': False,
        'show': False
    },
    flags=[
        CommandInput(
            '-f', '--force',
            action_func=mykey_func('force', True),
            final=True
        ),
        CommandInput(
            '-s', '--show',
            action_func=mykey_func('show', True),
            final=False,
            children=[
                OptionalVariableInputParam(
                    action_func=theirkey_func('name1'),
                    final=True,
                    terminal=True
                )
            ]
        )
    ],
    children=[
        OptionalVariableInputParam(
            action_func=theirkey_func('name1'),
            children=[
                OptionalVariableInputParam(
                    final=True,
                    terminal=True,
                    action_func=theirkey_func('name2')
                )
            ]
        )
    ]
)


SET_OS_TYPE = CommandInput(
        'os', 'set_os', 'setos',
        include_help=True,
        default_data={
            'command': cmd_set_os_type,
            'input1': None, 
            'input2': None,
            'reset': False,
            'show': False
            },
        flags=[
            CommandInput(
                '-r',
                action_func=mykey_func('reset', True),
                children=[
                    OptionalVariableInputParam(
                        action_func=theirkey_func('input1'),
                        final=True,
                        terminal=True
                        )
                    ]
                ),
            CommandInput(
                '-s',
                action_func=mykey_func('show', True),
                children=[
                    OptionalVariableInputParam(
                        action_func=theirkey_func('input1'),
                        final=True,
                        terminal=True
                        )
                    ]
                )
            ],
        children=[
            OptionalVariableInputParam(
                action_func=theirkey_func('input1'),
                children=[
                    OptionalVariableInputParam(
                        action_func=theirkey_func('input2'),
                        final=True,
                        terminal=True
                        )
                    ]
                )
            ]
        )


SET_HASH = CommandInput(
    'sethash', 'hash',
    include_help=True,
    default_data={
        'command': cmd_set_hash,
        'action': None
    },
    children=[
        VariableInputParam(
            action_func=theirkey_func('action'),
            final=True,
            terminal=True
        )
    ]
)


CMD_CD = CommandInput(
    'cd',
    include_help=True,
    default_data={
        'command': cmd_cd,
        'index': False,
        'first': None,
        'second': None
    },
    flags=[
        InputParam(
            '-i', '--index',
            action_func=mykey_func('index', True),
            final=True
        )
    ],
    children=[
        VariableInputParam(
            action_func=theirkey_func('first'),
            children=[
                OptionalVariableInputParam(
                    final=True,
                    terminal=True,
                    action_func=theirkey_func('second')
                )
            ]
        )
    ]
)

CMD_LS = CommandInput(
    'ls', 'dir',
    include_help=True,
    default_data={
        'command': cmd_ls,
        'index': False,
        'show_index': False,
        'recorded_only': False,
        'mtime': False,
        'first': None,
        'second': None
    },
    flags=[
        InputParam(
            '-r', '--recorded',
            action_func=mykey_func('recorded_only', True),
            final=True
        ),
        InputParam(
            '-i', '--index',
            action_func=mykey_func('index', True),
            final=True
        ),
        InputParam(
            '-I',
            action_func=mykey_func('show_index', True),
            final=True
        ),
        InputParam(
            '-m',
            action_func=mykey_func('mtime', True),
            final=True
        )
    ],
    children=[
        OptionalVariableInputParam(
            action_func=theirkey_func('first'),
            children=[
                OptionalVariableInputParam(
                    final=True,
                    terminal=True,
                    action_func=theirkey_func('second')
                )
            ]
        )
    ]
)


CMD_CDLS = CommandInput(
    'cdls',
    include_help=True,
    default_data = {
        'command': cmd_cdls,
        'index': False,
        'input1': None,
        'input2': None
    },
    flags=[
        InputParam(
            '-i', '--index',
            action_func=mykey_func('index', True),
            final=True
        )
    ],
    children=[
        VariableInputParam(
            action_func=theirkey_func('input1'),
            children=[
                OptionalVariableInputParam(
                    action_func=theirkey_func('input2'),
                    terminal=True
                )
            ]
        )
    ]
)


CMD_RECROOT = CommandInput(
    'recroot', 'newroot',
    include_help=True,
    default_data={
        'command': cmd_recroot,
        'index': False,
        'localpath': None,
        'treepath': None,
        'name': None
    },
    flags=[
        InputParam(
            '-n', '--name', '--nickname',
            action_func=blank_func(),
            children=[
                VariableInputParam(
                    final=True,
                    action_func=theirkey_func('name')
                )
            ]
        ),
        InputParam(
            '-p', '--path', '--treepath',
            action_func=blank_func(),
            children=[
                VariableInputParam(
                    final=True,
                    action_func=theirkey_func('treepath')
                )
            ]
        ),
        InputParam(
            '-i', '--index',
            action_func=mykey_func('index', True),
            final=True
        )
    ],
    children=[
        VariableInputParam(
            final=True,
            terminal=True,
            action_func=theirkey_func('localpath')
        )
    ]
)


CMD_SET_LOCALPATH = CommandInput(
    'local', 'localpath', 'set_localpath', 'root_localpath',
    include_help=True,
    default_data={
        'command': cmd_set_localpath,
        'root': None,
        'path': None
    },
    children=[
        VariableInputParam(
            action_func=theirkey_func('root'),
            children=[
                VariableInputParam(
                    action_func=theirkey_func('path'),
                    terminal=True
                )
            ]
        )
    ]
)


CMD_REC = CommandInput(
    'rec', 'record',
    include_help=True,
    default_data={
        'command': cmd_rec,
        'index': False,
        'cd': False,
        'cdls': False,
        'path': None,
        'use_localpath': False,
        'recursive': False,
        'r_levels': 0,
        'verbose': 0,
    },
    flags=[
        InputParam(
            '-i', '--index',
            action_func=mykey_func('index', True),
            final=True
        ),
        InputParam(
            '-l', '--local', '--use-local', '--localpath', '--use-localpath',
            final=True,
            action_func=mykey_func('use_localpath', True)
        ),
        InputParam(
            '-r', '--recursive',
            action_func=mykey_func('recursive', True),
            children=[
                VariableInputParam(
                    final=True,
                    action_func=theirkey_func('r_levels')
                )
            ]
        ),
        InputParam(
            '-RR',
            terminal=False,
            final=True,
            action_func=(lambda x, y: x | {'recursive': True, 'r_levels': -1})
        ),
        InputParam(
            '-a', '--all',
            final=True,
            terminal=True,
            action_func=lambda params, data: params | {'recursive': True, 'r_levels': 1, 'path': '.'} 
        ),
        InputParam(
            '-cd',
            final=True,
            action_func=mykey_func('cd', True)
        ),
        InputParam(
            '-cdls',
            final=True,
            action_func=mykey_func('cdls', True)
        ),
        InputParam(
            '-v', '--verbose',
            final=True,
            action_func=mykey_func('verbose', -1)
        ),
        InputParam(
            '-vv', '--verbose-levels',
            children=[
                VariableInputParam(
                    action_func=theirkey_func('verbose'),
                    final=True
                )
            ]
        )
    ],
    children=[
        VariableInputParam(
            final=True,
            terminal=True,
            action_func=theirkey_func('path')
        )
    ]
)


CMD_REMOVE = CommandInput(
    'remove',
    include_help=True,
    default_data={
        'command': cmd_remove,
        'index': False,
        'confirm': False,
        'path': None
    },
    flags=[
        InputParam(
            '-i', '--index',
            action_func=mykey_func('index', True),
            final=True
        ),
        InputParam(
            '-y', '--yes', '--confirm',
            action_func=mykey_func('confirm', True),
            final=True
        )
    ],
    children=[
        VariableInputParam(
            action_func=theirkey_func('path'),
            terminal=True
        )
    ]
)


CMD_SAVE = CommandInput(
        'save',
        include_help=True,
        default_data={
            'command': cmd_save,
            'tree': None,
            'all': False,
            'force': False,
            'pretty': False
            },
        flags=[
            InputParam(
                '-a', '--all',
                final=True,
                action_func=mykey_func('all', True)
                ),
            InputParam(
                '-f', '--force',
                final=True,
               action_func=mykey_func('force', True)
               ),
            InputParam(
                '-p', '--pretty',
                final=True,
                action_func=mykey_func('pretty', True)
                )
            ],
        children=[
            OptionalVariableInputParam(
                final=True,
                terminal=True,
                action_func=theirkey_func('tree')
                )
            ]
        )
        

DROP_TREE = CommandInput(
    'drop', 'droptree',
    include_help=True,
    default_data={
        'command': cmd_droptree,
        'tree': None,
        'force': False
    },
    flags=[
        CommandInput(
            '-f', '--force',
            final=True,
            action_func=mykey_func('force', True)
        )
    ],
    children=[
        VariableInputParam(
            final=True,
            terminal=True,
            action_func=theirkey_func('tree')
        )
    ]
)


PRINT_WORKING_TREE = CommandInput(
    'pwt',
    include_help=True,
    default_data = {
        'command': cmd_pwt
    },
    final=True
)


PRINT_WORKING_DIRECTORY = CommandInput(
    'pwd',
    include_help=True,
    default_data={
        'command': cmd_pwd,
        'tree': None,
        'full': False,
        'local': False
        },
    flags=[
        InputParam(
            '-f', '--full',
            action_func=mykey_func('full', True),
            final=True
            ),
        InputParam(
            '-l', '--local',
            action_func=mykey_func('local', True),
            final=True
            )
        ],
    children=[
        OptionalVariableInputParam(
            action_func=theirkey_func('tree'),
            final=True,
            terminal=True
            )
        ]
)

CHANGE_TREE = CommandInput(
    'chtree', 'cht', 'cdtree', 'cdt',
    include_help=True,
    default_data={
        'command': cmd_change_tree,
        'tree': None
    },
    children=[
        VariableInputParam(
            action_func=theirkey_func('tree'),
            final=True,
            terminal=True
        )
    ]
)


TIE_FILES = CommandInput(
    'tie',
    include_help=True,
    default_data={
        'command': cmd_tie,
        'index': False,
        'indexNum': None,
        'all': False,
        'tree': None,
        'source': None,
        'destination': None
    },
    flags=[
        InputParam(
            '-a', '--all',
            action_func=mykey_func('all', True),
            children=[
                VariableInputParam(
                    action_func=theirkey_func('tree'),
                    terminal=True
                    )
                ]
            ),
        InputParam(
            '-i', '--index',
            action_func=mykey_func('index', True),
            final=True,
            ),
        InputParam(
            '-I',
            children=[
                VariableInputParam(
                    action_func=theirkey_func('indexNum'),
                    final=True
                    )
                ]
            )
        ],
    children=[
        VariableInputParam(
            action_func=theirkey_func('source'),
            children=[
                VariableInputParam(
                    action_func=theirkey_func('tree'),
                    children=[
                        VariableInputParam(
                            action_func=theirkey_func('destination'),
                            final=True,
                            terminal=True
                        )
                    ]
                )
            ]
        )
    ]
)


CMD_INFO = CommandInput(
    'info',
    include_help=True,
    default_data={
        'command': cmd_info,
        'index': False,
        'input1': None,
        'input2': None,
        'amount': 'short',
        'sys_hash': False,
        'history': False,
        'ties': False
    },
    flags=[
        CommandInput(
            '-i', '--index',
            action_func=mykey_func('index', True),
            final=True
        ),
        CommandInput(
            # This is actually redundant, but I've already written it...
            '-l', '--long',
            action_func=mykey_func('amount', 'full'),
            final=True
        ),
        CommandInput(
            '-s', '--short',
            action_func=mykey_func('amount', 'short'),
            final=True
            ),
        CommandInput(
            '-H', '--do-hash',
            action_func=mykey_func('sys_hash', True),
            final=True
        ),
        CommandInput(
            '--history',
            action_func=mykey_func('history', True),
            final=True
            ),
        CommandInput(
            '--ties',
            action_func=mykey_func('ties', True),
            final=True
            )
    ],
    children=[
        VariableInputParam(
            action_func=theirkey_func('input1'),
            children=[
                OptionalVariableInputParam(
                    action_func=theirkey_func('input2'),
                    final=True,
                    terminal=True
                )
            ]
        )
    ]
)


CMD_HISTORY = CommandInput(
        'history', 'hist',
        include_help=True,
        default_data={
            'command': cmd_history,
            'index': False,
            'full': False,
            'input1': None,
            'input2': None
            },
        flags=[
            CommandInput(
                '-i', '--index',
                action_func=mykey_func('index', True),
                final=True,
            ),
            CommandInput(
                '-f', '--full',
                action_func=mykey_func('full', True),
                final=True
                )
            ],
        children=[
            VariableInputParam(
                action_func=theirkey_func('input1'),
                children=[
                    OptionalVariableInputParam(
                        action_func=theirkey_func('input2'),
                        terminal=True
                        )
                    ]
                )
            ]
        )


CMD_TIES = CommandInput(
    'ties',
    include_help=True,
    default_data={
        'command': cmd_print_ties,
        'index': True,
        'input1': None,
        'input2': None
        },
    flags=[
        CommandInput(
                '-i', '--index',
                action_func=mykey_func('index', True),
                final=True,
            ),
        ],
    children=[
        VariableInputParam(
            action_func=theirkey_func('input1'),
            children=[
                OptionalVariableInputParam(
                    action_func=theirkey_func('input2'),
                    terminal=True
                    )
                ]
            )
        ]
    )


UPDATE_ENTRY = CommandInput(
        'update',
        include_help=True,
        default_data={
            'command': cmd_update,
            'index': False,
            'path': '.',
            'recursive': False,
            'r_levels': 0,
            'all': False
            },
        flags=[
            CommandInput(
                '-i', '--index',
                action_func=mykey_func('index', True),
                final=True,
            ),
            InputParam(
                '-r', '--recursive',
                action_func=mykey_func('recursive', True),
                children=[
                    VariableInputParam(
                        action_func=theirkey_func('r_levels'),
                        final=True
                        )
                    ],
                ),
            InputParam(
                '-a', '--all',
                action_func=mykey_func('recursive', True),
                terminal=True
                ),
            InputParam(
                '-RR',
                action_func=lambda data, y: data | {'recursive': True, 'r_levels': -1},
                terminal=True
                )
            ],
        children=[
            OptionalVariableInputParam(
                action_func=theirkey_func('path'),
                terminal=True
                )
            ]
        )


CMD_AUTOUPDATE = CommandInput(
        'autoupdate', 'auto_update',
        include_help=True,
        default_data={
            'command': cmd_autoupdate,
            'show': False,
            'input1': None,
            'input2': None,
            },
        flags=[
            InputParam(
                '-s', '--show',
                action_func=theirkey_func('show'),
                children=[
                    OptionalVariableInputParam(
                        action_func=theirkey_func('input1'),
                        terminal=True
                        )
                    ]
                )
            ],
        children=[
            OptionalVariableInputParam(
                action_func=theirkey_func('input1'),
                children=[
                    OptionalVariableInputParam(
                        'input2',
                        action_func=theirkey_func('input2'),
                        terminal=True
                        )
                    ]
                )
            ]
        )


CMD_NOTES = CommandInput(
        'note',
        include_help=True,
        default_data={
            'command': cmd_notes,
            'index': False,
            'input1': None,
            'input2': None,
            'action': 'show'
            },
        flags=[
            CommandInput(
                '-i', '--index',
                action_func=mykey_func('index', True),
                final=True,
            ),
            CommandInput(
                '-a', '--add',
                action_func=mykey_func('action', 'add'),
                final=True
            ),
            CommandInput(
                '-r', '--remove',
                action_func=mykey_func('action', 'remove'),
                final=True
                )
            ],
        children=[
            VariableInputParam(
                action_func=theirkey_func('input1'),
                children=[
                    OptionalVariableInputParam(
                        action_func=theirkey_func('input2'),
                        terminal=True
                        )
                    ]
                )
            ]
        )


IGNORE_LIST = CommandInput(
    'ignore', 'ignorelist',
    include_help=True,
    default_data={
        'command': cmd_ignore,
        'remove': False,
        'index': False,
        'input': None
    },
    flags=[
        CommandInput(
            '-r', '--remove',
            action_func=mykey_func('remove', True),
            final=True
        ),
        CommandInput(
            '-i', '--index',
            action_func=mykey_func('index', True),
            final=True
        ),
        CommandInput(
            '-c', '--clear',
            action_func=mykey_func('clear', True),
            terminal=True
        )
    ],
    children=[
        OptionalVariableInputParam(
            action_func=theirkey_func('input'),
            terminal=True
        )
    ]
)



MainInputParser = InputParser(
    children = [
        BLANK,
        QUIT,
        CMD_HELP,
        ADD_TREE,
        CREATE_TREE,
        SET_SESSION_NAME,
        ACTIVATE_TREE,
        DEACTIVATE_TREE,
        ECHO,
        LIST_ALL_TREES,
        LIST_TREE,
        RENAME_TREE,
        ON_SYSTEM,
        OFF_SYSTEM,
        SET_SAVE_FILE,
        CMD_CD,
        CMD_LS,
        CMD_CDLS,
        CMD_RECROOT,
        CMD_SET_LOCALPATH,
        CMD_REC,
        CMD_REMOVE,
        CMD_SAVE,
        DROP_TREE,
        PRINT_WORKING_TREE,
        CHANGE_TREE,
        TIE_FILES,
        CMD_INFO,
        CMD_HISTORY,
        CMD_TIES,
        SET_HASH,
        SET_OS_TYPE,
        PRINT_WORKING_DIRECTORY,
        UPDATE_ENTRY,
        CMD_NOTES,
        CMD_AUTOUPDATE,
        IGNORE_LIST
    ]
)



cmd_confirmation_prompt = 'confirm_action'


CONFIRMATION_YES = CommandInput(
    'y', 'yes', 'continue', 'ok', 'okay', 'sure', 'yep', 'yeah', 'yup', 'true',
    case_sensitive=False,
    default_data=blank_dict(cmd_confirmation_prompt, 'confirm'),
    final=True,
    terminal=True,
    action_func=mykey_func('confirm', True)
)


CONFIRMATION_NO = CommandInput(
    '', ' ', 'n', 'no', 'cancel', 'stop', 'jk', 'nope', 'nah', 'nevermind', 'false',
    case_sensitive=False,
    default_data=blank_dict(cmd_confirmation_prompt, 'confirm'),
    final=True,
    terminal=True,
    action_func=mykey_func('confirm', False)
)


ConfirmationInputParser = InputParser(
    default_command=CONFIRMATION_NO,
    children=[
        CONFIRMATION_YES,
        CONFIRMATION_NO
    ]
)
