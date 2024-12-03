from setuptools import setup, find_packages

VERSION = '0.1.1'
DESCRIPTION = "OMEGAPy Python Toolkit all projects need"
INSTALL_REQUIRES = ["openai","vosk","SpeechRecognition","pyaudio","pydub","openai-whisper","pySmartDL"]


setup(name="omglib",
      version=VERSION,
      py_modules=['omglib'],
      description=DESCRIPTION,
      author="M1778",
      author_email="m1778.pc@gmail.com")