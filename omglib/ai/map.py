from .variables import *
import speech_recognition as _SR
import whisper as _whisper
from vosk import Model as _vosk_model, KaldiRecognizer as _kaldi
import pyaudio  
from pydub import AudioSegment

Microphone= _SR.Microphone
_R = _SR.Recognizer()

class Vosk:
    def __init__(self,model_language:str=Languages.English,model_size:str=VoskModelSize.Small):
        self._model=VoskModels.GetModel(model_language,model_size)
        self.options={'kaldi_h':16000}
    def install_model(self):
        return VMM.install_model(self._model,prints=True)
    def init(self):
        if self.install_model():
            self.recognizer = _kaldi(_vosk_model(self.load_model()),self.options['kaldi_h'])
            return True
        return False
    def load_model(self):
        return VMM.get_model_path(self._model)
    def set_model(self,model:dict):
        self._model = model
    def get_model(self):
        return self.recognizer
    def __call__(self):
        return self.get_model()


class Whisper:
    def __init__(self,whispermodel:str=WhisperModels.Base):
        self._whispermodel = whispermodel
    def load_model(self):
        self.recognizer = _whisper.load_model(self._whispermodel)
    def init(self):
        self.load_model()
        return True
    def get_model(self):
        return self.recognizer
    def __call__(self):
        return self.get_model()

class Wit:
    def __init__(self,apikey:str,apikey_language:str):
        self.apikey=apikey
        self.lang=apikey_language
    def recognize(self,audio_data):
        return _R.recognize_wit(audio_data,self.apikey)

class VoskAPI:
    def __init__(self,language:str='en'):
        self.language = language
    def recognize(self,audio_data):
        return _R.recognize_vosk(audio_data,self.language)

class Google:
    def __init__(self,language:str='en-US'):
        self.language=language
    def recognize(self,audio_data):
        return _R.recognize_google(audio_data,language=self.language)

class Sphinx:
    def __init__(self,language='en-US'):
        self.language= language
    def recognize(self,audio_data):
        return _R.recognize_sphinx(audio_data,self.language)


def convert_raw_to_audio_data(raw_audio: bytes, sample_rate: int, sample_width: int = 2,channels:int=1) -> _SR.AudioData:
    """
    Convert raw PCM audio data to speech_recognition.AudioData.

    Parameters:
        raw_audio (bytes): The raw PCM audio data.
        sample_rate (int): The sample rate of the audio.
        sample_width (int): The sample width in bytes (default is 2 for 16-bit audio).

    Returns:
        sr.AudioData: AudioData object compatible with speech_recognition.
    """

    # Convert raw audio to AudioData
    return _SR.AudioData(raw_audio, sample_rate, sample_width * channels)

def get_raw_audio(file_path: str, sample_rate: int = 16000) -> bytes:
    """
    Reads an audio file and returns it as raw audio data that can be used with PyAudio.

    Parameters:
        file_path (str): The path to the audio file.
        sample_rate (int): The desired sample rate for the audio.

    Returns:
        bytes: Raw PCM audio data that can be used with PyAudio.
    """
    try:
        # Load audio file with pydub
        audio = AudioSegment.from_file(file_path)

        # Convert to mono and set sample rate
        audio = audio.set_channels(1).set_frame_rate(sample_rate).set_sample_width(2)

        # Convert to raw data (PCM format)
        raw_data = audio.raw_data
        return raw_data

    except Exception as e:
        print(f"Error while processing the audio file: {e}")
        return b""

def play_raw_audio(raw_audio_data: bytes, sample_rate: int = 16000, channels: int = 1, sample_width: int = 2):
    """
    Plays raw audio data using PyAudio.

    Parameters:
        raw_audio_data (bytes): The raw PCM audio data to be played.
        sample_rate (int): The sample rate of the audio (default 16000 Hz).
        channels (int): Number of channels (1 for mono, 2 for stereo, etc., default is mono).
        sample_width (int): Sample width in bytes (default is 2 for 16-bit audio).
    """
    try:
        # Initialize PyAudio instance
        p = pyaudio.PyAudio()

        # Open a stream for playback
        stream = p.open(
            format=pyaudio.paInt16,  # 16-bit PCM format
            channels=channels,       # Mono or stereo
            rate=sample_rate,        # Sample rate (e.g., 16000)
            output=True              # Output stream
        )

        # Play the raw audio data in chunks
        stream.write(raw_audio_data)

        # Stop and close the stream
        stream.stop_stream()
        stream.close()

        # Terminate PyAudio
        p.terminate()

        print("Audio playback finished.")
    except Exception as e:
        print(f"Error during audio playback: {e}")

