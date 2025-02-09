import requests
from . import wmodels as models


class CloudFlareClient:
    def __init__(self,ACCOUNT_ID:str,AUTH_TOKEN:str):
        self.accid = ACCOUNT_ID
        self.autht = AUTH_TOKEN
        self.url = f"https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/ai/run/"
        self.headers = {"Authorization":f"Bearer {AUTH_TOKEN}"}
    def generate(self,model:str,messages:list,hyperparameters:dict={}):
        inputs = {"messages":messages}
        for param in hyperparameters.keys():
            inputs[param] = hyperparameters[param]
        response = requests.post(self.url+model,headers=self.headers,json=inputs)
        return response.json()['result']
    def agree_model(self,model:str=models.LLAMA_3_2_11B_VISION_INSTRUCT):
        return requests.post(self.url+model,headers=self.headers,json={"prompt":"agree"}).json()['result']
    