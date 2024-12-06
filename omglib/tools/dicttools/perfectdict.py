from ..listtools.listing import aget_only_item
class _wTempClass:name=None
def has_key(dict_:dict,key:any):return True if key in dict_.keys() else False
def nhas_key(dict_:dict,key:any):return False if key in dict_.keys() else True
def has_value(dict_:dict,value:any):return True if value in dict_.values() else False
def nhas_value(dict_:dict,value:any):return False if value in dict_.values() else True
def get_key(dict_:dict,key:any):return dict_[key] if has_key(dict_,key) else None
def get_keys(dict_:dict):return list(dict_.keys())
def get_values(dict_:dict):return list(dict_.values())
def has_keys(dict_:dict,keys:list):return True if all([key in keys for key in dict_.keys()]) else False
def nhas_keys(dict_:dict,keys:list):return False if all([key in keys for key in dict_.keys()]) else True
def nhas_atleast_onekey(dict_:dict,keys:list):return False if any([key in keys for key in dict_.keys()]) else True
def has_atleast_onekey(dict_:dict,keys:list):return True if any([key in keys for key in dict_.keys()]) else False
def wkey_has_prop(dict_:dict,property_name:str,property_value)->bool:ks,chks=[k for k in list(dict_.keys())],[hasattr(k,property_name) for k in list(dict_.keys())];return any([True if getattr(ks[ind] if isinstance(ind,int) else _wTempClass,'name') == property_value else False for ind in [i if chks[i] == True else None for i in range(len(chks))]])
def gkey_has_prop(dict_:dict,property_name:str,property_value)->bool:ks,chks=[k for k in list(dict_.keys())],[hasattr(k,property_name) for k in list(dict_.keys())];return aget_only_item([ks[ind] if getattr(ks[ind] if isinstance(ind,int) else _wTempClass,'name') == property_value else False for ind in [i if chks[i] == True else None for i in range(len(chks))]])
def key_ret(dict_:dict,key:any):return get_key(dict_,key) if has_key(dict_,key) else None