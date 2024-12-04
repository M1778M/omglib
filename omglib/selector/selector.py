from ..tools.dicttools import perfectdict

class SelectKeyExists(Exception):...
class SelectKeyDoesntExists(Exception):...
class InvalidSelectionValue(Exception):...


class Selector:
    def __init__(self,selector_name:str="SELECTOR"):
        self._SELECTOR_ = selector_name
    def __repr__(self):
        return f"<{self._SELECTOR_} {str(id(self))[-6:]}>"
    def _first_run(self,initial_config):
        if not hasattr(self,'_select_options'):
            self._select_options = initial_config
        return

class SelectKey:
    def __init__(self,name:str=None):
        if name == None:
            self.name=id(self)
        else:
            self.name = name
    def __call__(self):
        return self.name
    def __repr__(self):
        return f"<SelectKey name={self.name}>"

class DictSelector(Selector):
    _initial_config = {}
    def __init__(self):
        super().__init__("DictSelector")
        self._first_run(DictSelector._initial_config)
        self._recognize_by = 'name'
    def load_from_dict(self,dict_:dict):
        self._select_options = dict_
        return self
    def _safe_value(self,value):
        if type(value) in [int,str,bool,dict,list,float,complex,range,tuple,set,frozenset,bytes,bytearray,memoryview,type(None)]:
            return value
        else:
            raise InvalidSelectionValue(f"SAFEVALUE:-> Value '{value}' is not a valid/supported format for DictSelector, use 'bypass_safe_value' property to disable it.")
    def _safe_check(self,selkey:SelectKey):
        if perfectdict.has_key(self._select_options,selkey):
            raise SelectKeyExists(f"SAFECHECK:-> Key '{selkey}' exists in the DictSelector.")
        return True
    def add_selection(self,selection_key:SelectKey,selection_value:any,bypass_safe_check:bool=False,bypass_safe_value:bool=False):
        self._safe_check(selection_key) if bypass_safe_check == False else None
        self._select_options[selection_key] = self._safe_value(selection_value) if bypass_safe_value == False else selection_value
        self._select_options[selection_key] = selection_value
        return self
    def delete_selection(self,selection_key:SelectKey):
        if isinstance(selection_key,tuple) or isinstance(selection_key,list):
            for key in selection_key:
                self.delete_selection(key)
            return self
        if perfectdict.has_key(self._select_options,selection_key):
            del self._select_options[selection_key]
        return self
    @property
    def all(self):
        return self.select_all()
    def select_all(self):
        return self._select_options
    def select(self,selection_key:SelectKey):
        if selection_key == "*" and perfectdict.nhas_key(self._select_options,selection_key):
            return self._select_options
        if perfectdict.nhas_key(self._select_options,selection_key) and not perfectdict.wkey_has_prop(self._select_options,self._recognize_by,selection_key):
            raise SelectKeyDoesntExists(f"Key '{selection_key}' doesn't exist in the DictSelector.")
        if perfectdict.has_key(self._select_options,selection_key):
            return self._select_options[selection_key]
        if perfectdict.wkey_has_prop(self._select_options,self._recognize_by,selection_key):
            return self._select_options[perfectdict.gkey_has_prop(self._select_options,self._recognize_by,selection_key)]
        return self._select_options[selection_key]
    def __call__(self,selection_key:SelectKey=None,selection_value:any=None):
        if selection_key == None and selection_value == None:
            return self
        elif selection_key != None and selection_value == None:
            return self.select(selection_key)
        else: 
            return self.add_selection(selection_key,selection_value)
    def __matmul__(self,selection_key:SelectKey):
        return self.delete_selection(selection_key)
    def __iter__(self):
        for item in range(len(perfectdict.get_keys(self._select_options))):
            yield self._select_options[item]
    def __gt__(self,item:tuple):
        if type(item) is not tuple:return self.__call__(item)
        return self.__call__(*item)
    def __lt__(self,item:tuple):
        if type(item) is not tuple:return self.__call__(item)
        return self.__call__(*item)
    def __getitem__(self,item:SelectKey):
        return self.__call__(item)