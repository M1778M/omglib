from openai import OpenAI as _OPENAI
from .beta.workers import wmap
from mistralai import Mistral as _Mistral
import cohere
import requests
import json
tid_bk=1

class OpenAI:
    default_model = "gpt-4o-mini"
    def __init__(self,api_key:str):
        self.api_key = api_key
        self.client = _OPENAI(api_key=api_key)
        self.model=OpenAI.default_model
        self.messages = []
        self.tool_support = True
    def add_message(self,role:str,content:str):
        self.messages.append({'role':role,'content':content})
    def request(self,tools=[]):
        return self.client.chat.completions.create(messages=self.messages,tools=tools,tool_choice='auto',model=self.model).choices[0].message
    @staticmethod
    def tc_convert(response):
        return {'role':response['role'],'tool_calls':response['tool_calls']}
    @staticmethod
    def func_call(response,func_call):
        global tid_bk
        for call in response['tool_calls']:
            if not call['id']:
                call['id'] = str(tid_bk)
                tid_bk+=1
            yield func_call(call['function']['name'],json.loads(call['function']['arguments'])),call
    @staticmethod
    def func_call_response(tool_call,func_response):
        return {"role": "tool",
                    "tool_call_id": tool_call['id'],
                    "content": json.dumps(func_response)}
    def tool_handle(self,response,func_call):
        if not isinstance(response,dict):
            response=response.dict()
        if response['tool_calls']:
            addable = []
            addable.append(self.tc_convert(response))
            for ind,resp in enumerate(self.func_call(response,func_call)):
                addable.append(self.func_call_response(response['tool_calls'][ind],resp[0]))
            return addable
        else:
            return [response]
class DeepSeek:
    default_model = "deepseek-ai/DeepSeek-R1"
    def __init__(self,api_key):
        self.api_key = api_key
        self.client = _OPENAI(base_url="https://huggingface.co/api/inference-proxy/together",api_key=self.api_key)
        self.model = self.default_modela
        self.messages = []
        self.tool_support = False
        self.max_tokens = 100000
    def add_message(self,role:str,content:str):
        self.messages.append({'role':role,'content':content})
    def request(self,tools=[]):
        return self.client.chat.completions.create(model=self.model,messages=self.messages,max_tokens=self.max_tokens,tools=tools if tools else None)
    @staticmethod
    def tc_convert(response):
        return {'role':response['role'],'tool_calls':response['tool_calls']}
    @staticmethod
    def func_call(response,func_call):
        global tid_bk
        for call in response['tool_calls']:
            if not call['id']:
                call['id'] = str(tid_bk)
                tid_bk+=1
            yield func_call(call['function']['name'],json.loads(call['function']['arguments'])),call
    @staticmethod
    def func_call_response(tool_call,func_response):
        return {"role": "tool",
                    "tool_call_id": tool_call['id'],
                    "content": json.dumps(func_response)}
    def tool_handle(self,response,func_call):
        if not isinstance(response,dict):
            response=response.dict()
        if response['tool_calls']:
            addable = []
            addable.append(self.tc_convert(response))
            for ind,resp in enumerate(self.func_call(response,func_call)):
                addable.append(self.func_call_response(response['tool_calls'][ind],resp[0]))
            return addable
        else:
            return [response]

class CloudFlare:
    default_model = wmap.models.LLAMA_31_70B_INSTRUCT
    def __init__(self,account_id:str,api_key):
        self.api_key = api_key
        self.account_id = account_id
        self.client = wmap.CloudFlareClient(account_id,api_key)
        self.model=CloudFlare.default_model
        self.messages=[]
        self.tool_support = False
    def add_message(self,role:str,content:str):
        self.messages.append({'role':role,'content':content})
    def request(self,tools=[]):
        resp=self.client.generate(self.model,self.messages,{'tools':tools,'tool_choice':'auto'})
        if 'tool_calls' in list(resp.keys()):
            return {'role':'assistant','content':resp['response'] if resp['response'] else '','tool_calls':resp['tool_calls']}
        return {'role':'assistant','content':resp['response'] if 'response' in resp.keys() and resp['response'] else ''}
    @staticmethod
    def tc_convert(response):
        return {'role':response['role'],'content':response['content']}
    @staticmethod
    def func_call(response,func_call):
        global tid_bk
        for call in response['tool_calls']:
            call['id']=tid_bk
            tid_bk+=1
            yield func_call(call['name'],call['arguments']),call
    @staticmethod
    def func_call_response(tool_call,func_response):
        return {"role": "tool",
                    "content": json.dumps(func_response)}
    def tool_handle(self,response,func_call):
        if not isinstance(response,dict):
            response=response.dict()
        if response['tool_calls']:
            addable = []
            addable.append(self.tc_convert(response))
            for ind,resp in enumerate(self.func_call(response,func_call)):
                addable.append(self.func_call_response(response['tool_calls'][ind],resp[0]))
            return [self.tc_convert(self.request())]
        else:
            return [response]
class Groq:
    default_model = "llama-3.1-70b-versatile"
    def __init__(self,api_key:str):
        self.api_key = api_key
        self.client = _OPENAI(api_key=api_key,base_url=f"https://api.groq.com/openai/v1")
        self.model=Groq.default_model
        self.messages = []
        self.tool_support = True
    def add_message(self,role:str,content:str):
        self.messages.append({'role':role,'content':content})
    def request(self,tools=[]):
        return self.client.chat.completions.create(messages=self.messages,tools=tools,tool_choice='auto',model=self.model).choices[0].message
    @staticmethod
    def tc_convert(response):
        return {'role':response['role'],'tool_calls':response['tool_calls']}
    @staticmethod
    def func_call(response,func_call):
        global tid_bk
        for call in response['tool_calls']:
            if not call['id']:
                call['id'] = str(tid_bk)
                tid_bk+=1
            yield func_call(call['function']['name'],json.loads(call['function']['arguments'])),call
    @staticmethod
    def func_call_response(tool_call,func_response):
        return {"role": "tool",
                    "tool_call_id": tool_call['id'],
                    "content": json.dumps(func_response)}
    def tool_handle(self,response,func_call):
        if not isinstance(response,dict):
            response=response.dict()
        if response['tool_calls']:
            addable = []
            addable.append(self.tc_convert(response))
            for ind,resp in enumerate(self.func_call(response,func_call)):
                addable.append(self.func_call_response(response['tool_calls'][ind],resp[0]))
            return addable
        else:
            return [response]

class TogetherAI:
    default_model = "meta-llama/Llama-3.3-70B-Instruct-Turbo"
    def __init__(self,api_key:str):
        self.api_key = api_key
        self.client = _OPENAI(api_key=api_key,base_url=f"https://api.together.xyz/v1")
        self.model=TogetherAI.default_model
        self.messages = []
        self.tool_support = True
    def add_message(self,role:str,content:str):
        self.messages.append({'role':role,'content':content})
    def request(self,tools=[]):
        return self.client.chat.completions.create(messages=self.messages,tools=tools,tool_choice='auto',model=self.model).choices[0].message
    @staticmethod
    def tc_convert(response):
        return {'role':response['role'],'tool_calls':response['tool_calls']}
    @staticmethod
    def func_call(response,func_call):
        global tid_bk
        for call in response['tool_calls']:
            if not call['id']:
                call['id'] = str(tid_bk)
                tid_bk+=1
            yield func_call(call['function']['name'],json.loads(call['function']['arguments'])),call
    @staticmethod
    def func_call_response(tool_call,func_response):
        return {"role": "tool",
                    "tool_call_id": tool_call['id'],
                    "content": json.dumps(func_response)}
    def tool_handle(self,response,func_call):
        if not isinstance(response,dict):
            response=response.dict()
        if response['tool_calls']:
            addable = []
            addable.append(self.tc_convert(response))
            for ind,resp in enumerate(self.func_call(response,func_call)):
                addable.append(self.func_call_response(response['tool_calls'][ind],resp[0]))
            return addable
        else:
            return [response]

class AvianAI:
    default_model = "Meta-Llama-3.3-70B-Instruct"
    def __init__(self,api_key:str):
        self.api_key = api_key
        self.client = _OPENAI(api_key=api_key,base_url=f"https://api.avian.io/v1")
        self.model=AvianAI.default_model
        self.messages = []
        self.tool_support = True
    def add_message(self,role:str,content:str):
        self.messages.append({'role':role,'content':content})
    def request(self,tools=[]):
        return self.client.chat.completions.create(messages=self.messages,tools=tools,tool_choice='auto',model=self.model).choices[0].message
    @staticmethod
    def tc_convert(response):
        return {'role':response['role'],'tool_calls':response['tool_calls']}
    @staticmethod
    def func_call(response,func_call):
        global tid_bk
        for call in response['tool_calls']:
            if not call['id']:
                call['id'] = str(tid_bk)
                tid_bk+=1
            yield func_call(call['function']['name'],json.loads(call['function']['arguments'])),call
    @staticmethod
    def func_call_response(tool_call,func_response):
        return {"role": "tool",
                    "tool_call_id": tool_call['id'],
                    "content": json.dumps(func_response)}
    def tool_handle(self,response,func_call):
        if not isinstance(response,dict):
            response=response.dict()
        if response['tool_calls']:
            addable = []
            addable.append(self.tc_convert(response))
            for ind,resp in enumerate(self.func_call(response,func_call)):
                addable.append(self.func_call_response(response['tool_calls'][ind],resp[0]))
            return addable
        else:
            return [response]

class Cohere:
    default_model = "command-r-plus"
    def __init__(self,api_key:str):
        self.api_key = api_key
        self.client = cohere.ClientV2(api_key=api_key)
        self.model=Cohere.default_model
        self.messages = []
        self.tool_support = True
    def add_message(self,role:str,content:str):
        self.messages.append({'role':role,'content':content})
    def request(self,tools=[]):
        return self.client.chat(messages=self.messages,tools=tools,model=self.model).message
    @staticmethod
    def tc_convert(response):
        return {
            "role": "assistant",
            "tool_calls": response['tool_calls'],
            "tool_plan": response['tool_plan']}
    @staticmethod
    def func_call(response,func_call):
        for call in response['tool_calls']:
            yield func_call(call['function']['name'],json.loads(call['function']['arguments'])),call
    @staticmethod
    def func_call_response(tool_call,func_response):
        return {
            "role": "tool",
            "tool_call_id": tool_call['id'],
            "content": [{"type":"document","document":{"data":json.dumps(func_response)}}]
        }
    def tool_handle(self,response,func_call):
        if not isinstance(response,dict):
            response=response.dict()
        if response['tool_calls']:
            addable = []
            addable.append(self.tc_convert(response))
            for ind,resp in enumerate(self.func_call(response,func_call)):
                addable.append(self.func_call_response(response['tool_calls'][ind],resp[0]))
            return addable
        else:
            return [response]
    
class Mistral:
    default_model = "mistral-large-latest"
    def __init__(self,api_key:str):
        self.api_key = api_key
        self.client = _OPENAI(api_key=api_key,base_url='https://api.mistral.ai/v1/chat/completions')
        self.model=Mistral.default_model
        self.messages = []
        self.tool_support = True
    def add_message(self,role:str,content:str):
        self.messages.append({'role':role,'content':content})
    def request(self,tools=[]):
        return self.client.chat.completions.create(messages=self.messages,tools=tools,tool_choice='auto',model=self.model).choices[0].message
    @staticmethod
    def tc_convert(response):
        return {'role':response['role'],'tool_calls':response['tool_calls']}
    @staticmethod
    def func_call(response,func_call):
        global tid_bk
        for call in response['tool_calls']:
            if not call['id']:
                call['id'] = str(tid_bk)
                tid_bk+=1
            yield func_call(call['function']['name'],json.loads(call['function']['arguments'])),call
    @staticmethod
    def func_call_response(tool_call,func_response):
        return {"role": "tool",
                    "tool_call_id": tool_call['id'],
                    "content": json.dumps(func_response)}
    def tool_handle(self,response,func_call):
        if not isinstance(response,dict):
            response=response.dict()
        if response['tool_calls']:
            addable = []
            addable.append(self.tc_convert(response))
            for ind,resp in enumerate(self.func_call(response,func_call)):
                addable.append(self.func_call_response(response['tool_calls'][ind],resp[0]))
            return addable
        else:
            return [response]
    
class OpenRouter:
    default_model = "google/gemini-2.0-flash-exp:free"
    def __init__(self,api_key:str):
        self.api_key = api_key
        self.client = _OPENAI(api_key=api_key,base_url="https://openrouter.ai/api/v1")
        self.model=OpenRouter.default_model
        self.messages = []
        self.tool_support = True
    def add_message(self,role:str,content:str):
        self.messages.append({'role':role,'content':content})
    def request(self,tools=[]):
        return self.client.chat.completions.create(messages=self.messages,tools=tools,tool_choice='auto',model=self.model).choices[0].message
    @staticmethod
    def tc_convert(response):
        return {'role':response['role'],'tool_calls':response['tool_calls']}
    @staticmethod
    def func_call(response,func_call):
        global tid_bk
        for call in response['tool_calls']:
            if not call['id']:
                call['id'] = str(tid_bk)
                tid_bk+=1
            yield func_call(call['function']['name'],json.loads(call['function']['arguments'])),call
    @staticmethod
    def func_call_response(tool_call,func_response):
        return {"role": "tool",
                    "tool_call_id": tool_call['id'],
                    "content": json.dumps(func_response)}
    def tool_handle(self,response,func_call):
        if not isinstance(response,dict):
            response=response.dict()
        if response['tool_calls']:
            addable = []
            addable.append(self.tc_convert(response))
            for ind,resp in enumerate(self.func_call(response,func_call)):
                addable.append(self.func_call_response(response['tool_calls'][ind],resp[0]))
            return addable
        else:
            return [response]
class Gemini:
    default_model = "models/gemini-2.0-flash"
    def __init__(self,api_key:str):
        self.api_key = api_key
        self.client = _OPENAI(api_key=api_key,base_url="https://generativelanguage.googleapis.com/v1beta/openai/")
        self.model=Gemini.default_model
        self.messages = []
        self.tool_support = True
    def add_message(self,role:str,content:str):
        self.messages.append({'role':role,'content':content})
    def request(self,tools=[]):
        return self.client.chat.completions.create(messages=self.messages,tools=tools,tool_choice='auto',model=self.model).choices[0].message
    @staticmethod
    def tc_convert(response):
        return {'role':response['role'],'tool_calls':response['tool_calls']}
    @staticmethod
    def func_call(response,func_call):
        global tid_bk
        for call in response['tool_calls']:
            if not call['id']:
                call['id'] = str(tid_bk)
                tid_bk+=1
            yield func_call(call['function']['name'],json.loads(call['function']['arguments'])),call
    @staticmethod
    def func_call_response(tool_call,func_response):
        return {"role": "tool",
                    "tool_call_id": tool_call['id'],
                    "content": json.dumps(func_response)}
    def tool_handle(self,response,func_call):
        if not isinstance(response,dict):
            response=response.dict()
        if response['tool_calls']:
            addable = []
            addable.append(self.tc_convert(response))
            for ind,resp in enumerate(self.func_call(response,func_call)):
                addable.append(self.func_call_response(response['tool_calls'][ind],resp[0]))
            return addable
        else:
            return [response]
# Additional functions

