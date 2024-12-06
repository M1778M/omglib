import json
import json.tool
import json.scanner
import requests
import python_weather
import asyncio
import serpapi
from pathlib import Path

from ..tools.dicttools import perfectdict

# Built in functions ---------------------------------------------
def convert_path(path:str): # Converts linux path to windows path
    return str(Path(path).absolute())
def init_inuse_tools_import():
    global m
    import win32ui
    import windowsapps
    import winapps
    m.win32ui = win32ui
    m.windowsapps = windowsapps
    m.winapps = winapps
#-----------------------------------------------------------------


global ALL_AVAILABLE_TOOLS
_debug = True

FunctionConfigs = {"search_web":{'apikey':None}}

class m:...

class XConfig:
    def set_search_web_apikey(apikey:str):
        FunctionConfigs['search_web']['apikey'] = apikey
        return True
    def add_search_web():
        ALL_AVAILABLE_TOOLS.append(gen_func("search_web",required=["query"],query=xtype(str,"the query for web search example: 'Top premiere leagues'"),search_engine=xtype(str,"The search engine to use for search example: 'google'",enum=['google','bing']),country_code=xtype(str,"The country code for regional search default:'US'"))) # search_web(query:str,search_engine:str='google',country_code:str="US")
        return True

def OpenApp(appname:str)->bool:
    try:
        m.windowsapps.open_app(appname) # Uses a library to search and open application
        return {"OpenApplicationStatus":"Successful","RequestedApplicationName":appname} # returns true if the application is found and launched 
    except:
        return {"OpenApplicationStatus":"Failed/Probaby not found","RequestedApplicationName":appname} # returns false if the application is not found

def ListInstalledAppsName()->list:
    output=[] # the return variable
    for app in list(m.winapps.list_installed()): # loops through installed applications using "winapps" library
       output.append(app.name) # appends only the name of the applications installed
    return {"ApplicationsList":output} # returns the names of the applications installed

def UninstallApp(appname:str)->bool:
    if m.winapps.search_installed(appname)==[]:return False # Returns false if installed application is not found
    
    ask=m.win32ui.MessageBox(f"Do you really want to uninstall {appname}?","AI Assistant",4) # makes sure if user wants their application to be deleted
    if ask == 6:
        try:
            m.winapps.uninstall(appname) # uninstalls the application
            return {"UninstallAppRequest":"Successful","RequestedApplication":appname}
        except:
            return {"UninstallAppRequest":"Failed","RequestedApplication":appname,"Reason":"Probably due to being unable to locate the application or application doesn't exist."}
    else:
        return {"UninstallAppRequest":"Failed","RequestedApplication":appname,"Reason":"User rejected the verification to uninstall their application"}

def MessageBox(message:str,title:str,style:int=0)->dict:
    _= m.win32ui.MessageBox(message,title,style) # Shows MessageBox with arguements
    # checks for codes for answers and returns simpler answers
    if _ == 1:
        return {"MessageBoxStatus":"Shown_Successfully","MessageBoxReturnCode":_,"MessageBoxReturnCode_Translation":"OK_BUTTON"}
    elif _ == 2:
        return {"MessageBoxStatus":"Shown_Successfully","MessageBoxReturnCode":_,"MessageBoxReturnCode_Translation":"CANCEL_BUTTON"}
    elif _ == 3:
        return {"MessageBoxStatus":"Shown_Successfully","MessageBoxReturnCode":_,"MessageBoxReturnCode_Translation":"ABORT_BUTTON"}
    elif _ == 4:
        return {"MessageBoxStatus":"Shown_Successfully","MessageBoxReturnCode":_,"MessageBoxReturnCode_Translation":"RETRY_BUTTON"}
    elif _ == 5:
        return {"MessageBoxStatus":"Shown_Successfully","MessageBoxReturnCode":_,"MessageBoxReturnCode_Translation":"IGNORE_BUTTON"}
    elif _ == 6:
        return {"MessageBoxStatus":"Shown_Successfully","MessageBoxReturnCode":_,"MessageBoxReturnCode_Translation":"YES_BUTTON"}
    elif _ == 7:
        return {"MessageBoxStatus":"Shown_Successfully","MessageBoxReturnCode":_,"MessageBoxReturnCode_Translation":"NO_BUTTON"}
    elif _ == 10:
        return {"MessageBoxStatus":"Shown_Successfully","MessageBoxReturnCode":_,"MessageBoxReturnCode_Translation":"TRYAGAIN_BUTTON"}
    elif _ == 11:
        return {"MessageBoxStatus":"Shown_Successfully","MessageBoxReturnCode":_,"MessageBoxReturnCode_Translation":"CONTINUE_BUTTON"}
    else:
        return {"MessageBoxStatus":"Suspended","MessageBoxReturnCode":_,"MessageBoxReturnCode_Translation":"UNKNOWN"}

def run_py(python_code:str):
    run_status = "Successful"
    error_message = "<No Error>"
    try:
        exec(python_code)
    except Exception as e:
        run_status = "Failed"
        error_message=e
    return {"run_status":run_status,"error_message":error_message}

async def _get_weather(location:str,unit:str='celcius'):
    cli=python_weather.Client(unit=python_weather.constants.METRIC if unit == "celcius" else python_weather.constants.IMPERIAL)
    weather=await cli.get(location=location)
    return {"location":weather.location,"temperature":weather.temperature,"unit":unit,"datetime":weather.datetime.strftime("%Y-%m-%d %H:%M:%S"),"additional_data":{"kind":str(weather.kind),"description":weather.description,"country":weather.country,"coordinates":list(weather.coordinates)}}

def get_weather(location:str,unit:str='celcius'):
    if asyncio.get_event_loop().is_closed():
        asyncio.set_event_loop(asyncio.new_event_loop())
    return asyncio.get_event_loop().run_until_complete(_get_weather(location=location,unit=unit))

def search_web(query:str,search_engine:str='google',country_code:str="US"): # Searches the web with English language results
    if FunctionConfigs['search_web']['apikey'] == None:
        return {"Error":"Failed","Further_Details_DEV":"User hasn't set any api key for search_web option, reject them or guide them."}
    if search_engine.lower() == 'google':
        results = {"query":query,"search_engine":search_engine,"search_results":{},"discussions_and_forums":{},"related_questions":{}}
        try:
            json_results=serpapi.GoogleSearch({'q':query
                  ,'api_key':'c1cc10ba909b3eda11d791d2fe5a6a4f32a3518830447dc68f634f36b27af4a9'
                  ,'device':'desktop'
                  ,'gl':country_code}).get_json()
            if perfectdict.has_key(json_results,'error'):
                return json_results
            for sr in json_results['organic_results']:
                results["search_results"][sr['position']] = {'title':sr['title'],'link':sr['link'],'snippet':perfectdict.key_ret(sr,'snippet')}
            if perfectdict.has_key(json_results,'related_questions'):
                for rq in json_results['related_questions']:
                    results["related_questions"][rq['question']] = {'title':rq['title'],'snippet':rq['snippet'],'date':perfectdict.key_ret(rq,'date'),'link':rq['link']}
            if perfectdict.has_key(json_results,'discussions_and_forums'):
                for daf in range(len(json_results['discussions_and_forums'])):
                    results['discussions_and_forums'][daf] = {'title':json_results['discussions_and_forums'][daf]['title'],'link':json_results['discussions_and_forums'][daf]['link'],'date':perfectdict.key_ret(json_results['discussions_and_forums'][daf],'date')}
            return results
        except Exception as e:
            if _debug:
                print("Error in google: ",e)
            return {"Error":"Failed","Further_Details_DEV":e}
    elif search_engine.lower() == 'bing':
        results = {"query":query,"search_engine":search_engine,"search_results":{}}
        try:
            json_results = serpapi.BingSearch({'q':query
                  ,'api_key':'c1cc10ba909b3eda11d791d2fe5a6a4f32a3518830447dc68f634f36b27af4a9'
                  ,'device':'desktop'
                  ,'cc':country_code}).get_json()
            if perfectdict.has_key(json_results,'error'):
                return json_results
            for sr in json_results['organic_results']:
                results["search_results"][sr['position']] = {'title':sr['title'],'link':sr['link'],'snippet':perfectdict.key_ret(sr,'snippet')}
            return results
        except Exception as e:
            if _debug:
                print("Error in bing: ",e)
            return {"Error":"Failed","Further_Details_DEV":e}
    else:
        return {"Error":"Failed","Further_Details_DEV":e}



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
        "content":func_output
    }

ALL_AVAILABLE_TOOLS = [
    gen_func("run_py","Runs the given python code using 'exec' function",python_code=xtype(str,"The python code to run"))  ,
    gen_func("get_weather","Returns the current weather of input location",required=['location'],location=xtype(str,"the location to get the weather for, examples : 'Tehran','New York'"),unit=xtype(str,"The unit of temperature example: celcius",enum=['celcius','fahrenheit'])),
    gen_func("MessageBox","Shows a message box client-side to user using (pywin32.win32ui)",required=["message","title"],message=xtype(str,"The message shown in message box"),title=xtype(str,"The title shown for message box window"),style=xtype(int,"The style of the message box based on win32ui.MessageBox style policy range from 0 to 6. 0 being a basic message box with [ok] button and 1 being [ok,cancel] and so on...",enum=[0,1,2,3,4,5,6])),
    gen_func("OpenApp","Opens an application by searching the given name example: Notepad",appname=xtype(str,"The name of the application you want to open")) ,
    gen_func("ListInstalledAppsName","Returns a list of all applications installed on system"),
    gen_func("UninstallApp","Ask user for verification before uninstalling the given app",appname=xtype(str,"The name of the application you want to uninstall example:Pycharm")),
    
]

def call_func(func_name:str,**func_args):
    return globals()[func_name](**func_args)