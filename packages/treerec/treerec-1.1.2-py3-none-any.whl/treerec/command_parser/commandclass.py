from treerec.command_parser.madout import Madout
from copy import copy

"""
Class functions for programmatically building up command options,
with built-in error handling.
"""

# this combination is chosen as the name for an InputParam that takes a variable,
# because it is unlikely to be used in a command, or as the name of a file
varkey = "\\#!&*^/\\~\n"

QUOTE_CHARS = ['"', "'"]

def terminate_after_flag(func):
    def terminate_wrapper(slf, tokens, idx, data):
        data['final'] = True
        return func(slf, tokens, idx, data)
    return terminate_wrapper


def combine_quotes(tokens:list) -> list:
    """
    Combines all entries in input that are surrounded by double quotes.
    """
    tokens_out = []
    idx = 0
    while idx < len(tokens):
        word = tokens[idx]
        if len(word) != 0 and word[0] in QUOTE_CHARS:
            quotechar = word[0]
            if len(word) > 1 and word[-1] == quotechar:
                tokens_out.append(word[1:-1])
            else:
                phrase = [word[1:]]
                for idx2, word2 in enumerate(tokens[idx+1:]):
                    if len(word2) != 0 and word2[-1] == quotechar:
                        phrase.append(word2[:-1])
                        idx += (idx2 + 1)
                        break
                    else:
                        phrase.append(word2)
                new_word = ' '.join(phrase)
                tokens_out.append(new_word)
        else:
            tokens_out.append(word)
        idx += 1
    return tokens_out


def get_next_token(tokens:list, idx:int):
    idx += 1
    if len(tokens) <= idx:
        return False, False
    cmd = tokens[idx]
    while cmd == '':
        idx += 1
        if len(tokens) <= idx:
            return False, False
        cmd = tokens[idx]
    return cmd, idx


class InputParam():
    """
    Expects a list input of strings, which can be cast into certain types.
    Depending on the input, it decides which InputParam in its child list
        to pass the rest of the statement onto.
    """
    def __init__(self,
                 *param_names,
                 case_sensitive=True,
                 final=False,
                 terminal=False,
                 action_func=lambda data, tokens: data,
                 children=[]):
        if not case_sensitive:
            self.params = list(map(str.lower, param_names))
        else:
            self.params = param_names  # the string(s) which activate this
        self.case_sensitive = case_sensitive
        self.path_final = final  # is the command complete after this parameter has been entered?
        self.is_terminal = terminal  # should the command exit immediately after this parameter (and its children)# ?
        self.children = {}  # list of parameters which come after this one
        self.action = action_func  # function to be called if this is the final parameter
        self.has_optional_children = False
        self.is_optional = False
        for child in children:
            self.add_param(child)
    
    def __getitem__(self, name):
        return self.children[name]

    def set_action(self, func):
        self.action = func

    def add_param(self, param):
        for name in param.params:
            self.children[name] = param
        if param.is_optional:
            self.has_optional_children = True

    def execute(self, intokens:list, idx:int, data={}):
        #  Input should be a list of nonempty strings, the first of which is in self.params
        data = self.action(data, intokens[idx])
        #  Including intokens[0] in self.action covers the case where it is a variable
        cmd_test, idx_test = get_next_token(intokens, idx)
        if self.is_terminal:
            return self.goto_no_more_params(intokens, idx, data)
        if self.has_optional_children:
            return self.goto_optional_next_param(intokens, idx, data)
        if self.path_final:
            #  self.path_final==True when this is the last parameter of a parameter chain
            #  (e.g. a flag), but not necessarily the last parameter of the command.
            return Madout(True, "", idx, data, False)
            #  All Output should be Madout objects with three data entries:
            #   index of the current command in intokens,
            #   data to be passed to the next parameter,
            #   whether the command is complete (self.is_terminal).
        return self.goto_required_next_param(intokens, idx, data)

    def goto_required_next_param(self, intokens:list, idx:int, data={}):
        prev = intokens[idx]
        cmd, idx = get_next_token(intokens, idx)
        if cmd == False:
            return Madout(False,
                          'Expected more input after "' + prev + '".',
                          idx, data, False)
        next_param = self.find_next_param(cmd)
        if not next_param:
            return Madout(False,
                          'Unrecognized command after "' + prev + '": ' + cmd,
                          idx, data, False)
        return next_param.execute(intokens, idx, data)

    def goto_optional_next_param(self, intokens:list, idx:int, data={}):
        """
        Optional parameter(s) should always be at the very end of a command.
        """
        prev = intokens[idx]
        cmd, idx_new = get_next_token(intokens, idx)
        if cmd == False:
            return Madout(True, "", idx, data, True)
        next_param = self.find_next_param(cmd)
        if not next_param:
            return Madout(True, "", idx, data, True)
        return next_param.execute(intokens, idx_new, data)

    def goto_no_more_params(self, intokens:list, idx:int, data={}):
        prev = intokens[idx]
        cmd, idx = get_next_token(intokens, idx)
        if cmd == False:
            return Madout(True, "", idx, data, True)
        return Madout(False, 'Unexpected input after "' + prev + '": ' + cmd, idx, data, False)

    def find_next_param(self, cmd):
        if self.children.get(cmd, False):
            return self.children.get(cmd,False)
        if nextparam := self.children.get(cmd.lower(), False):
            if not nextparam.case_sensitive:
                return nextparam
        if self.children.get(varkey, False):
            return self.children[varkey]
        return False


class OptionalInputParam(InputParam):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.is_optional = True


class VariableInputParam(InputParam):
    def __init__(self, *args, **kwargs):
        super().__init__(varkey, *args, **kwargs)


class OptionalVariableInputParam(OptionalInputParam):
    def __init__(self, *args, **kwargs):
        super().__init__(varkey, *args, **kwargs)


help_flags = ['-h', '-help', '--h', '--help']


class CommandInput(InputParam):
    """
    Takes a list of strings, and passes the rest onto the correct line of InputParams.
    match_param pops the leftmost one off
    There should only be one child that has a matching type of 'int' or 'float'
    """
    def __init__(self,
                 *args,
                 flags=[],
                 default_data={},
                 include_help=False,
                 **kwargs):
        super().__init__(*args, **kwargs)
        self.default_data = default_data
        self.flags = {}
        for flag in flags:
            self.add_flag(flag)
        if include_help:
            self.default_data = self.default_data | {'help': False}
            self.add_flag(InputParam(
                *help_flags,
                final=True,
                terminal=True,
                action_func=lambda d,t: d | {'help':True} 
            ))

    def add_flag(self, inparam):
        for name in inparam.params:
            self.flags[name] = inparam

    def find_next_flag(self, cmd):
        if self.flags.get(cmd, False):
            return self.flags[cmd]
        return False

    def execute(self, intokens: list, idx: int, data=None):
        if data==None:
            data = copy(self.default_data)
        #  In a command, the action should be to set the default data fields
        data = self.action(data, intokens[0])
        mad_flag = self.flag_loop(intokens, idx, data)
        if not mad_flag or mad_flag[2]:
            return mad_flag
        #  We decide to still check for flags, even if the command is terminal.
        #  This allows flags to otherwise argument-less commands, like pwd.
        if self.is_terminal:
            return self.goto_no_more_params(intokens, idx, data)
        idx = mad_flag[0]
        data = mad_flag[1]
        if self.has_optional_children:
            return self.goto_optional_next_param(intokens, idx, data)
        if self.path_final:
            return Madout(True, "", idx, data, False)
        return self.goto_required_next_param(intokens, idx, data)

    def flag_loop(self, intokens: list, idx: int, data={}):
        """
        This function is called when the command is a flag.
        It loops through all flags in the command, and executes them.
        """
        prev = intokens[idx]
        while True:
            cmd, idx_new = get_next_token(intokens, idx)
            if cmd == False:
                return Madout(True, "", idx, data, False)
                #  We'll deal with this case directly in self.execute
            next_flag = self.find_next_flag(cmd)
            if not next_flag:
                return Madout(True, "", idx, data, False)
            new_mad = next_flag.execute(intokens, idx_new, data)
            if not new_mad or new_mad[2]:
                return new_mad
            idx = new_mad[0]
            data = new_mad[1]

    def passdown(self, intokens:list, idx:int, data={}):
        prev = intokens[idx]
        cmd, idx = get_next_token(intokens, idx)
        while self.flags.get(cmd, False):
            mad, idx = self.flags[cmd].execute(intokens, idx, data)
            data = mad.result()
            if idx==False:
                return mad
            cmd, idx = get_next_token(intokens, idx)
        if idx==False and self.has_optional_children:
            return Madout(True, "", data), idx
        if self.optional_children.get(cmd, False):
            mad, idx = self.optional_children[cmd].execute(data, intokens, idx)
            data = mad.result()
            cmd, idx = get_next_token(intokens, idx)
            if idx==False:
                return mad
        if self.children.get(cmd, False):
            return self.children[cmd].execute(intokens, idx, data)
        if self.children.get(varkey, False):
            return self.children[varkey].execute(intokens, idx, data)
        return Madout(False, 'Error: unrecognized command after "' + prev + '": ' + cmd)


class InputParser():
    def __init__(self, children=[], default_command=None):
        self.children = {}
        for child in children:
            self.add_command(child)
        self.default_command = default_command

    def __call__(self, instr: str) -> Madout:
        return self.execute(instr)
    
    def add_default_command(self, command:CommandInput):
        self.default_command = command

    def execute(self, instr:str) -> Madout:
        intokens = instr.split(' ')
        # we need to split on spaces, specifically, because then
        # the resulting list includes empty strings for each space.
        # this allows us to handle the edge case of a file name with
        # multiple consecutive spaces in it.
        intokens = combine_quotes(intokens)
        cmd, idx = get_next_token(intokens, -1)
        if cmd == False:
            if self.children.get('', False):
                return self.children[''].execute(intokens, 0, None)
            return Madout(False, "", False, None)
        if self.children.get(cmd, None):
            return self.children[cmd].execute(intokens, idx, None)
        elif self.default_command:
            return self.default_command.execute(intokens, idx, None)
        else: 
            return Madout(False, "Unknown command: " + cmd, False, None)

    def add_command(self, command):
        for name in command.params:
            self.children[name] = command

