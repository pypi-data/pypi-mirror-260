import os
import platform

from gtts import gTTS
from playsound import playsound

from toolboxv2 import get_app
from toolboxv2.mods.audio.TBV2TTS.audioProvider.ElevenLapsProviderPy import ElevenLapsProvider

try:
    import pyttsx3

    pyttsx3_init = True
except ImportError:
    pyttsx3_init = False

Name = 'audio.tts.mini'
version = "0.0.2"
export = get_app(f"{Name}.EXPORT").tb
no_test = export(mod_name=Name, test=False, version=version)
test_only = export(mod_name=Name, test_only=True, version=version, state=True)
to_api = export(mod_name=Name, api=True, version=version)

_simpel_speech_recognizer = None
_simpel_speech_recognizer_mice = None
eleven_laps_provider = ElevenLapsProvider()


@no_test
def text_to_speech(text, lang='de'):
    tts = gTTS(text=text, lang=lang)
    if platform.system() == "Darwin" or platform.system() == "Linux":
        filename = f"{get_app(from_=f'{Name}.isaa.audio.get_data_dir').data_dir}/Audio/speech.mp3"
    else:
        filename = f"{get_app(from_=f'{Name}.isaa.audio.get_data_dir').data_dir}/Audio\\speech.mp3"
    tts.save(filename)
    playsound(filename)
    os.remove(filename)


@no_test
def text_to_speech3(text):
    if pyttsx3_init:
        def text_to_speech3_(text, engine=pyttsx3.init()):
            engine.say(text)
            engine.runAndWait()
            return engine

        return text_to_speech3_(text)
    else:
        print("TTS 3 not available")
