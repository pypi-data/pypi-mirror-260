import queue
import subprocess
import tempfile
import os
import threading
from typing import Dict

from tqdm import tqdm

from toolboxv2 import Style
from toolboxv2.mods.audio.TBV2TTS.util import _play_from_cache, save_audio_to_cache, play_audio_bytes, get_hash_key
from toolboxv2.mods.audio.utils import split_text_x_symbol


def find_onnx_files(start_path):
    onnx_dict = {}

    # Rekursive Funktion, um durch die Ordner zu navigieren
    def search_dir(path):
        for item in os.listdir(path):
            item_path = os.path.join(path, item)
            if os.path.isdir(item_path):
                # Wenn das Element ein Ordner ist, suche rekursiv weiter
                search_dir(item_path)
            else:
                # Überprüfe, ob die Datei eine .onnx Datei ist und eine entsprechende .json Datei existiert
                if item.endswith('.onnx'):
                    json_filename = item + '.json'
                    if json_filename in os.listdir(path):
                        # Entferne die Dateiendung und speichere den Pfad
                        file_name_without_extension = ''.join(item.split('.')[:-1])
                        onnx_dict[file_name_without_extension] = os.path.abspath(item_path).replace('.onnx', '')

    # Starte die Suche vom Startpunkt
    search_dir(start_path)
    return onnx_dict

class PiperInterface:

    def __init__(self, models: Dict[str, str] = None, audio_player: str = None, piper_path: str = './piper.exe',
                 default_model_path: str = None, verbose: bool = False):

        self.verbose = verbose
        if audio_player is None:
            self.audio_player = 'cmdmp3' if os.name == 'nt' else 'mpg123'  # Standard-Audioplayer für Windows und Unix-basierte Systeme
        else:
            self.audio_player = audio_player

        if models is None:
            self.models = {}  # Standard-Modellpfade können hier definiert werden
        else:
            self.models = models

            self.piper_path = piper_path
        self.default_model_path = default_model_path
        self.v_print("Startet PiperInterface")

    def v_print(self, *args, **kwargs):
        if not self.verbose:
            return
        print(Style.MAGENTA("Verbose:piper"), end=" ")
        print(*args, **kwargs)

    def text_to_speech(self, text: str, cache: bool = True, config: dict or None = None, delete=True):

        play_local = True
        do_generate = True
        cache_generator = None

        if config is None:
            config = {
                'voice_index': 0,
                'noise_scale': 0.667,
                'length_scale': 1.0,
                'noise_width': 0.8,
                'sentence_silence': 0.2,
                'model_path': self.default_model_path
            }
        elif 'play_local' in config:
            play_local = config['play_local']
            del config['play_local']

        if 'model_path' in config:
            config['model_path'] = self.models.get(config['model_path'], self.default_model_path)

        if 'model_path' not in config:
            config['model_path'] = self.default_model_path

        if cache:
            cache_generator = _play_from_cache(text, play_local)
            do_generate = not next(cache_generator)

        if do_generate:
            audio_data = self._generate_audio(text, delete=delete, **config)
            if cache:
                save_audio_to_cache(get_hash_key(text), audio_data)
            if play_local:
                play_audio_bytes(audio_data, format_="wav")
            else:
                return audio_data

        if not play_local and cache and cache_generator is not None and not do_generate:
            audio_data = next(cache_generator)
            cache_generator.close()
            return audio_data

    def worker(self, _text, _id='0', _cache=True, _config=None):
        self.v_print("Worker Online", _id)
        filename = self.text_to_speech(text=_text, cache=_cache, config=_config, delete=False)
        self.v_print("Worker Done", _id)
        return filename

    def text_to_speech_stram(self, text: str, cache: bool = True, config: dict or None = None):
        texts = split_text_x_symbol(text=text, symbol='\n', split_n=2)
        len_texts = len(texts)
        if config is None:
            config = {}
        config_ = config.copy() if config else {}
        play_local = config_.get('play_local', True)
        _threaded = config_.get('threaded', True)

        que_text_data = queue.Queue()
        que_file_name = queue.Queue()

        self.v_print("Text splittet in", len_texts, "parts")

        if len_texts == 1:
            config__ = {
                'voice_index': config.get('voice_index', 0),
                'noise_scale': config.get('noise_scale', 0.667),
                'length_scale': config.get('length_scale', 1.0),
                'noise_width': config.get('noise_width', 0.8),
                'sentence_silence': config.get('sentence_silence', 0.2),
                'model_path': config.get('model_path', self.default_model_path),
            }
            self.text_to_speech(text=text, cache=cache, config=config__, delete=False)

        def worker_helper():
            worker_idx = 0
            running = True
            self.v_print("WorkerHelper online")

            while que_text_data.not_empty and running:
                self.v_print("WorkerHelper Received data")
                text_data = que_text_data.get()
                config___ = {
                    'voice_index': config.get('voice_index', 0),
                    'noise_scale': config.get('noise_scale', 0.667),
                    'length_scale': config.get('length_scale', 1.0),
                    'noise_width': config.get('noise_width', 0.8),
                    'sentence_silence': config.get('sentence_silence', 0.2),
                    'model_path': config.get('model_path', self.default_model_path),
                    'play_local': False,
                }
                file_name = self.worker(text_data, str(worker_idx), cache, config___.copy()).decode()
                que_file_name.put(file_name)
                worker_idx += 1
                print("WorkerHelper index", worker_idx, len_texts, worker_idx >= len_texts, '\n')
                if worker_idx >= len_texts:
                    running = False
            self.v_print("WorkerHelper exit")
            print("WorkerHelper exit")

        threading.Thread(target=worker_helper, daemon=True).start()

        if not play_local:
            for i in range(len_texts):
                que_text_data.put(texts[i])
            return que_file_name

        que_text_data.put(texts[0])

        def local_player():
            running_player = True
            iteration = 0
            self.v_print("Starting Player")
            with tqdm(total=len_texts, unit='chunk', desc='Processing data') as pbar:
                print("Process Player", running_player, bool(que_file_name.not_empty))
                while que_file_name.not_empty and running_player:
                    output_file = que_file_name.get()
                    pbar.write(output_file)
                    with open(output_file, 'rb') as f:
                        audio_content = f.read()
                        self.v_print("len audio content:", len(audio_content), type(audio_content))
                    os.unlink(output_file)
                    self.v_print("removed", output_file)
                    iteration += 1
                    if iteration < len_texts:
                        que_text_data.put(texts[iteration])
                    else:
                        self.v_print("Player closing...")
                        running_player = False
                    if cache:
                        save_audio_to_cache(get_hash_key(text), audio_content)
                    play_audio_bytes(audio_content, format_="wav")
                    pbar.update()
                self.v_print("Player exited")

        if _threaded:
            threading.Thread(target=local_player, daemon=True).start()
        else:
            return local_player

    def _generate_audio(self, text: str,
                        model_path: str,
                        delete=False,
                        voice_index=0,
                        noise_scale=0.667,
                        length_scale=1.0,
                        noise_width=0.8,
                        sentence_silence=0.2) -> bytes:

        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as output_file:
            piper_command = [
                self.piper_path,
                '--model', model_path,
                # '--speaker', str(voice_index),
                # '--noise_scale', str(noise_scale),
                # '--length_scale', str(length_scale),
                # '--noise_w', str(noise_width),
                # '--sentence_silence', str(sentence_silence),
                '--output_file', output_file.name,
            ]
            p = subprocess.Popen(piper_command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            try:
                stdout, stderr = p.communicate(input=text.encode('utf-8'), timeout=30)
            except subprocess.TimeoutExpired:
                p.kill()
                return b''

            self.v_print("stderr", stderr.decode('utf-8'))
            self.v_print("stdout - saved to", stdout.decode('utf-8'))

        if not delete:
            return output_file.name.encode('utf-8')

        with open(output_file.name, 'rb') as f:
            audio_content = f.read()
            self.v_print("len audio content:", len(audio_content), type(audio_content))

        os.unlink(output_file.name)
        self.v_print("removed", output_file.name)

        return audio_content


if __name__ == '__main__':
    start_path_ = r'C:\Users\Markin\Workspace\piper_w\models'
    onnx_files_dict = find_onnx_files(start_path_)
    print(onnx_files_dict)
    # models = {
    #     'thorsten_m': r'C:\Users\Markin\Workspace\piper_w\models\de\thorsten_m\de_DE-thorsten-medium.onnx'
    # }
    # piper_path = r'C:\Users\Markin\Workspace\piper_w\piper.exe'
    # tts = PiperInterface(models=models, piper_path=piper_path, default_model_path=models['de_DE-thorsten-medium'], verbose=False)
    # te = """Fast alle Produkte haben Eigenschaften, die erst durch ihr Fehlen auffallen. Ihre Anwesenheit führt nicht
    # zu besonderer Zufriedenheit, ihre Abwesenheit hingegen zu großem Frust. Diese Selbstverständlichkeiten heißen
    # „Hygienefaktoren“, ein Begriff, der zurückgeht auf den amerikanischen Psychologen Frederick Herzberg. Exit"""
    # tts.v_print("test")
    # tts.text_to_speech_stram(te, cache=False)
    # tts.v_print("test")
