from treerec.engine.engine_base import TreeEngine_Base
from pathlib import *
import json


def touch_file(filepath:str) -> bool:
    try:
        with open(filepath,'a') as file:
            file
        return True
    except Exception as error:
        print("Error with file: ", filepath, " : ", error)
        raise error


def new_update_file(pathlike:Path):
    if pathlike.exists():
        print("ERROR: File already exists.")
        return None
    try:
        with open(pathlike, 'w') as file:
            file.write('{}')
    except Exception as error:
        print("ERROR in making new update file: ", error)
        return None
    update_data = load_update_file(pathlike)
    return update_data


def load_update_file(pathlike:Path):
    if not pathlike.exists():
        print("ERROR: File does not exist.")
        return None
    try:
        with open(pathlike, 'r') as file:
            update_data = json.load(file)
    except Exception as error:
        print("ERROR in reading new update file: ", error)
        return None
    return update_data


class TreeEngine_Pending(TreeEngine_Base):

    # Extends MultiTreeHolder to include the use of an update file,
    # Which records events that may affect other trees that are not loaded.
    # E.g., moving a file that is tied to a file in an unloaded tree - 
    #   the file in the unloaded tree needs it's ties changed.
    
    
    # The update data is a dict, where the keys are the UUIDs of the trees.
    # Each element of the dict is a list of updates. Each update is a histevent,
    #   which will be interpreted by the MultiTreeHolder when the tree is loaded.

    def __init__(self, update_file_path:str, session:str=None, new_multitree:bool=False):
        super().__init__(session)
        self.update_data = None
        self.update_file_pathlike = full_Path(update_file_path)
        if new_multitree:
            self.update_data = new_update_file(self.update_file_pathlike)
        else:
            self.update_data = load_update_file(self.update_file_pathlike)
        
    def set_update_file(self, filename:str):
        if self.update_data is not None:
            print("ERROR: cannot set new update file when there is already update data loaded.")
            return
        pathlike = full_Path(filename)
        self.update_data = load_update_file(pathlike)
    
    def set_new_update_file(self, filename:str):
        if self.update_data is not None:
            print("ERROR: cannot create and set new update file when there is already update data loaded.")
            return
        pathlike = full_Path(filename)
        self.update_data = new_update_file(pathlike)
        
    
    ### adding events to the update data.
    ### relevant functions are: move, rename, delete
    
    
                
            
