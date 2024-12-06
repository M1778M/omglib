import requests
import json
import pyaudio
from pydub import AudioSegment
from io import BytesIO


def play_mp3_bytes(mp3_data: bytes):
    """
    Play MP3 audio data from a bytes object using PyAudio.
    
    :param mp3_data: MP3 audio data as bytes
    """
    # Decode MP3 bytes to raw audio data
    audio = AudioSegment.from_file(BytesIO(mp3_data), format="mp3")

    # Extract raw audio data and parameters
    raw_data = audio.raw_data
    sample_width = audio.sample_width
    frame_rate = audio.frame_rate
    channels = audio.channels
    
    # Initialize PyAudio
    p = pyaudio.PyAudio()
    
    # Open a PyAudio stream
    stream = p.open(format=p.get_format_from_width(sample_width),
                    channels=channels,
                    rate=frame_rate,
                    output=True)
    
    # Play the raw audio data
    stream.write(raw_data)
    
    # Stop and close the stream
    stream.stop_stream()
    stream.close()
    
    # Terminate PyAudio
    p.terminate()

class MurfAI:
    def __init__(self,apikey:str):
        self.apikey=apikey
        self.url = "https://api.murf.ai/v1/speech/generate"
    def get_file(self,text:str,lang:str="en-US-natalie",rate:int=0,pitch:int=0,samplerate:int=48000,style:str="Conversational"):
        payload=json.dumps({
  "voiceId": lang,
  "style": style,
  "text": text,
  "rate": rate,
  "pitch": pitch,
  "sampleRate": samplerate,
  "format": "MP3",
  "channelType": "MONO",
  "pronunciationDictionary": {},
  "encodeAsBase64": False,
  "variation": 1,
  "audioDuration": 0,
  "modelVersion": "GEN2"
})
        headers = {
  'Content-Type': 'application/json',
  'Accept': 'application/json',
  'api-key': self.apikey
}
        response=requests.request("POST",self.url,headers=headers,data=payload)
        return response.text
    def speak(self,text:str,lang:str="en-US-natalie",rate:int=0,pitch:int=0,samplerate:int=48000,style:str="Promo"):
        self.audioFile=json.loads(self.get_file(text,lang,rate,pitch,samplerate,style))['audioFile']
        audioData = requests.get(self.audioFile).content
        self.last_audio = audioData
        return play_mp3_bytes(audioData)

class Playht:
    def __init__(self,userid:str,secretkey:str):
        self._userid = userid
        self._secretkey = secretkey
        self.voiceid="s3://voice-cloning-zero-shot/2a7ddfc5-d16a-423a-9441-5b13290998b8/novasaad/manifest.json"
    def speak(self,text:str):
        headers={
            "X-USER-ID":self._userid,
            "AUTHORIZATION":self._secretkey,
            "accept":"audio/mpeg",
            "content-type":"application/json"
        }
        payload={
            "text":text,
            "voice_engine":"Play3.0",
            "voice":self.voiceid,
            "output_format":"mp3"
        }

        self.audioData=requests.request("POST","https://api.play.ht/api/v2/tts/stream",headers=headers,data=json.dumps(payload)).content
        return play_mp3_bytes(self.audioData)

    def get_voices(self):
        headers={
            "X-USER-ID":self._userid,
            "AUTHORIZATION":self._secretkey,
            "accept":"application/json"
        }
        return requests.get("https://api.play.ht/api/v2/voices",headers=headers).json()

