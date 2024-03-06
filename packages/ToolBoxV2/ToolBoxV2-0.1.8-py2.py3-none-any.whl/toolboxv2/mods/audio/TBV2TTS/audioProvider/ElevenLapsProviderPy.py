import requests
import os
from toolboxv2.mods.audio.TBV2TTS.util import get_hash_key, load_cache_file, play_audio_bytes, save_audio_to_cache, save_cache_file, play_audio_stream_bytes

version = "0.0.2"


class ElevenLapsProvider:

    def __init__(self, voices=None):
        if voices is None:
            voices = ["ErXwobaYiN019PkySvjV", "EXAVITQu4vr4xnSDxMaL", "9Mi9dBkaxn2pCIdAAGOB"]
        self.voices = voices

    def eleven_labs_speech_cache(self, text, voice_index=0, cache=True, play_local=True):
        hash_key = get_hash_key(text)
        cache_data = load_cache_file()

        if cache and hash_key in cache_data:
            audio_content = self._get_audio_from_history_item(cache_data[hash_key])
            if play_local:
                play_audio_bytes(audio_content)
            else:
                return audio_content
        else:
            audio_content_stram = self.eleven_labs_speech_stream(text, voice_index, play_local)
            if play_local:
                play_audio_bytes(audio_content_stram)
            else:
                return audio_content_stram
            self.add_last_audio_to_cache()

        return True

    def eleven_labs_speech(self, text, voice_index=0, play_local=True):
        tts_headers = {
            "Content-Type": "application/json",
            "xi-api-key": os.getenv("ELEVENLABS_API_KEY")
        }
        tts_url = "https://api.elevenlabs.io/v1/text-to-speech/{voice_id}".format(
            voice_id=self.voices[voice_index])
        formatted_message = {"text": text}

        hash_key = get_hash_key(text)
        cache_data = load_cache_file()

        if hash_key in cache_data:
            audio_content = self._get_audio_from_history_item(cache_data[hash_key])
        else:
            response = requests.post(
                tts_url, headers=tts_headers, json=formatted_message)

            if response.status_code != 200:
                print("Request failed with status code:", response.status_code)
                print("Response content:", response.content)
                return False

            audio_content = response.content
            save_audio_to_cache(text, audio_content)
        if play_local:
            play_audio_bytes(audio_content)
        else:
            return audio_content
        return True

    def eleven_labs_speech_stream(self, text, voice_index=0, play_local=True):
        tts_headers = {
            "Content-Type": "application/json",
            "xi-api-key": os.getenv("ELEVENLABS_API_KEY")
        }
        tts_url = "https://api.elevenlabs.io/v1/text-to-speech/{voice_id}/stream".format(
            voice_id=self.voices[voice_index])
        formatted_message = {"text": text}

        response = requests.post(
            tts_url, headers=tts_headers, json=formatted_message, stream=True)

        if response.status_code == 200:
            if play_local:
                play_audio_stream_bytes(response.raw)
            else:
                return response.raw
            return True
        else:

            print("Request failed with status code:", response.status_code)
            print("Response content:", response.content)
            return False

    @staticmethod
    def _get_history():
        history_url = "https://api.elevenlabs.io/v1/history"
        headers = {
            "Content-Type": "application/json",
            "xi-api-key": os.getenv("ELEVENLABS_API_KEY")
        }
        response = requests.get(history_url, headers=headers)

        if response.status_code == 200:
            return response.json()
        else:
            print("Request failed with status code:", response.status_code)
            print("Response content:", response.content)
            return None

    @staticmethod
    def _get_audio_from_history_item(history_item_id):
        audio_url = f"https://api.elevenlabs.io/v1/history/{history_item_id}/audio"
        headers = {
            "Content-Type": "application/json",
            "xi-api-key": os.getenv("ELEVENLABS_API_KEY")
        }
        response = requests.get(audio_url, headers=headers)

        if response.status_code == 200:
            return response.content
        else:
            print("Request failed with status code:", response.status_code)
            print("Response content:", response.content)
            return None

    def add_last_audio_to_cache(self):
        try:
            item = self._get_history()["history"][0]

            hash_key = get_hash_key(item["text"])

            cache_data = load_cache_file()

            if hash_key not in cache_data:
                history_id = item["history_item_id"]

                if history_id is not None:
                    save_audio_to_cache(hash_key, history_id)
        except TypeError:
            print("Error loading history (elevenlabs)")

    def generate_cache_from_history(self):
        history = self._get_history()
        if history is None:
            return

        cache_data = load_cache_file()

        len_c = len(cache_data)

        for item in history["history"]:
            hash_key = get_hash_key(item["text"])
            if hash_key not in cache_data:
                history_id = item["history_item_id"]

                if history_id is None:
                    continue

                print("hash key : ", hash_key)
                cache_data[hash_key] = history_id

        print(f"Adding {len(cache_data) - len_c} audio files to cache")

        save_cache_file(cache_data)
