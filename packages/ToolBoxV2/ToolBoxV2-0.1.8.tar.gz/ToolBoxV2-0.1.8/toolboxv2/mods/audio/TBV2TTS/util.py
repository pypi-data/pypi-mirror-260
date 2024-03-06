import hashlib
import os
import pickle
import tempfile
from io import BytesIO

from pydub import AudioSegment
from pydub.playback import play

from toolboxv2 import get_app

try:
    import pyttsx3

    pyttsx3_init = True
except ImportError:
    pyttsx3_init = False

try:
    import whisper

    whisper_init = True
except Exception:
    whisper_init = False

try:
    import winsound

    winsound_init = True
except ImportError:
    winsound_init = False

Name = 'audio.tts.utils'
_audio_tbv2tts_ulis_chash_data = None


def play_audio_bytes(audio_content, format_="mp3"):
    audio = AudioSegment.from_file(BytesIO(audio_content), format=format_)
    play(audio)


def play_audio_stream_bytes(audio_stream, format_="mp3"):
    with tempfile.NamedTemporaryFile(delete=False, suffix="."+format_) as temp_file:
        temp_file.write(audio_stream.read())
        temp_file.flush()
        audio = AudioSegment.from_file(temp_file.name, format=format_)
        play(audio)


def get_hash_key(text):
    return hashlib.md5(text.encode('utf-8')).hexdigest()


def load_cache_file():
    if _audio_tbv2tts_ulis_chash_data is not None:
        return _audio_tbv2tts_ulis_chash_data
    if os.path.exists(f"{get_app(from_=f'{Name}.audio.get_data_dir').data_dir}/cache_file.pkl"):
        with open(f"{get_app(from_=f'{Name}.audio.get_data_dir').data_dir}/cache_file.pkl", "rb") as f:
            return pickle.load(f)
    return {}


def save_cache_file(cache_data):
    with open(f"{get_app(from_=f'{Name}.audio.get_data_dir').data_dir}/cache_file.pkl", "wb") as f:
        pickle.dump(cache_data, f)


def save_audio_to_cache(hash_key, audio_content):
    cache_data = load_cache_file()
    cache_data[hash_key] = audio_content
    save_cache_file(cache_data)


def _play_from_cache(text, play_sound=True):
    cache_key = get_hash_key(text)
    cache_data = load_cache_file()

    if cache_key in cache_data:
        yield True
        audio_content = cache_data[cache_key]
        if play_sound:
            play_audio_bytes(audio_content)
        else:
            return audio_content
    yield False
