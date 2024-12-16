from openai import OpenAI
import json


class BasicAPI:
    def __init__(self,base_url:str,apikey:str,model_name:str,tools_use:bool=False):
        self.client = OpenAI(base_url=base_url,api_key=apikey)
        self.model = model_name
        self.max_tokens = 8000
        self.messages=[]
        self.tools = []
        self.tools_use = tools_use
    def system_message(self,content):
        self.messages.append({"role":"system","content":content})
        return True
    def user_message(self,content):
        self.messages.append({"role":"user","content":content})
        return True
    def set_tools(self,tools_list:list,tool_handle):
        self.tools_use = True
        self.tools = tools_list
        self.tool_handle_function = tool_handle
        return True
    def assistant_message(self):
        if not self.tools_use:
            comp = self.client.chat.completions.create(messages=self.messages,model=self.model,max_tokens=self.max_tokens)
            response = comp.choices[0].message
            self.messages.append({"role":response.role,"content":response.content})
            return response.content
        else:
            comp = self.client.chat.completions.create(messages=self.messages,model=self.model,max_tokens=self.max_tokens,tools=self.tools,tool_choice="auto")
            response = comp.choices[0].message
            if response.tool_calls:
                tool_call_id = response.tool_calls[0].id
                func_response=self.tool_handle_function(response.tool_calls.function.name,json.loads(response.tool_calls.function.arguments))
                self.messages.append(dict(response))
                self.messages.append({
                    'role':'tool',
                    'content':json.dumps(func_response),
                    'tool_call_id':tool_call_id
                })
                return self.assistant_message()
            else:
                self.messages.append({"role":response.role,"content":response.content})
                return response.content


class BasicCustom_API:
    def __init__(self,custom_api_client:OpenAI,model_name:str,tools_use:bool=False):
        self.client = custom_api_client
        self.model = model_name
        self.max_tokens = 8000
        self.messages=[]
        self.tools = []
        self.tools_use = tools_use
    def system_message(self,content):
        self.messages.append({"role":"system","content":content})
        return True
    def user_message(self,content):
        self.messages.append({"role":"user","content":content})
        return True
    def set_tools(self,tools_list:list,tool_handle):
        self.tools_use = True
        self.tools = tools_list
        self.tool_handle_function = tool_handle
        return True
    def assistant_message(self):
        if not self.tools_use:
            comp = self.client.chat.completions.create(messages=self.messages,model=self.model,max_tokens=self.max_tokens)
            response = comp.choices[0].message
            self.messages.append({"role":response.role,"content":response.content})
            return response.content
        else:
            comp = self.client.chat.completions.create(messages=self.messages,model=self.model,max_tokens=self.max_tokens,tools=self.tools,tool_choice="auto")
            response = comp.choices[0].message
            if response.tool_calls:
                tool_call_id = response.tool_calls[0].id
                func_response=self.tool_handle_function(response.tool_calls.function.name,json.loads(response.tool_calls.function.arguments))
                self.messages.append(dict(response))
                self.messages.append({
                    'role':'tool',
                    'content':json.dumps(func_response),
                    'tool_call_id':tool_call_id
                })
                return self.assistant_message()
            else:
                self.messages.append({"role":response.role,"content":response.content})
                return response.content
