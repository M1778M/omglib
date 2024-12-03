def has_key(dict_:dict,key:any):
    return True if key in dict_.keys() else False

def has_value(dict_:dict,value:any):
    return True if value in dict_.values() else False

def get_key(dict_:dict,key:any):
    return dict_[key] if has_key(dict_,key) else None

def get_keys(dict_:dict):
    return list(dict_.keys())

def has_keys(dict_:dict,keys:list):
    return True if all([key in keys for key in dict_.keys()]) else False

def has_atleast_onekey(dict_:dict,keys:list):
    return True if any([key in keys for key in dict_.keys()]) else False
