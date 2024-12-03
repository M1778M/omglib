from openai import OpenAI
import speech_recognition as _SR


class oWhisper:
    def __init__(self,apikey:str,language:str='en',model:str='whisper-1'):
        self._openai = OpenAI(api_key=apikey)
        self.model=model
        self.language=language
    def transcribe(self,raw_audio:str):
        return self._openai.audio.transcriptions.create(file=raw_audio,model=self.model,language=self.language)['text']


class GoogleCloudAPI:
    def __init__(self,json_creds:str,language:str='en'):
        self.json_creds=json_creds
        self.language=language
        self._R = _SR.Recognizer()
    def recognize(self,audio_data):
        return self._R.recognize_google_cloud(audio_data,credentials_json=self.json_creds,language=self.language)

