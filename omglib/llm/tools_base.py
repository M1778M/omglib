import json


# Formatation Section...
class TTArray:
    def __init__(self,items_type:type):
        self.items_type=items_type
    @property
    def t(self):
        return self.items_type

def xtype(type_,description:str,enum:list=None):
    if description == 'no_desc':
        if type_ == str and enum != None:
            return {"type":"string","enum":enum}
        elif type_ == int and enum != None:
            return {"type":"integer","enum":enum}
        elif type_ == float and enum != None:
            return {"type":"float","enum":enum}
        elif type_ == str:
            return {"type":"string"}
        elif type_ == int:
            return {"type":"integer"}
        elif type_ == float:
            return {"type":"float"}
        elif isinstance(type_,TTArray):
            return {"type":"array","items":type_.t}
        else:
            raise ValueError("Invalid value for xtype.argumentParser")
    if type_ == str and enum != None:
        return {"type":"string","enum":enum,"description":description}
    elif type_ == int and enum != None:
        return {"type":"integer","enum":enum,"description":description}
    elif type == float and enum != None:
        return {"type":"float","enum":enum,"description":description}
    elif type_ == str:
        return {"type":"string","description":description}
    elif type_ == int:
        return {"type":"integer","description":description}
    elif type_ == float:
        return {"type":"float","description":description}
    elif isinstance(type_,TTArray):
        return {"type":"array","description":description,"items":type_.t}
    else:
        raise ValueError("Invalid value for xtype.argumentParser")

def gen_func(func_name:str,func_desc:str,required=all,**kwargs): # example -> gen_func("insert_members",required=["mname","mbudget"],mname=xtype(str,"member name"),mbudget=xtype(int,"member budget in us dollars",enum=[100,200,300,400]),keywords=xtype(TTArray(xtype(str,"no_desc")),"keyword"))
    properties = {}
    for key in kwargs:
        properties[key] = kwargs[key]
    
    return {
        "type": "function",
        "function": {
            "name": func_name,
            "description":func_desc,
            "parameters": {
                "type": "object",
                "properties": properties,
                "required": required if required != all else list(kwargs.keys()),
                "additionalProperties": False,
            },
        },
    }
def gen_func_response(tool_call_id:str,func_name:str,func_output:json): # out.choices[0].message.tool_calls[n].id
    return {
        "tool_call_id":tool_call_id,
        "role":"tool",
        "name":func_name,
        "content":func_output if isinstance(func_output,str) else json.dumps(func_output)
    }
