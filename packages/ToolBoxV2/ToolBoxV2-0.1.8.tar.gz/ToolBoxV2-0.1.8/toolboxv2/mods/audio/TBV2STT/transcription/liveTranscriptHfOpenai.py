import os
import tempfile
import threading
import wave

import torch

PIPLINE = None

from toolboxv2 import get_logger, Style, get_app
import openai
import time
import pyaudio
import queue

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

import numpy as np

Name = 'audio.stt.live'
version = "0.0.2"


def get_mean_amplitude(stream, seconds=2, rate=44100, p=False):
    amplitude = []
    frames = []
    for j in range(int(rate / int(rate / 10) * seconds)):
        data = stream.read(int(rate / 10))
        frames.append(data)
        audio_np = np.frombuffer(data, dtype=np.int16)
        amplitude.append(np.abs(audio_np).mean())
        if p:
            print(
                f"[last amplitude] : {amplitude[-1]:.2f} "
                f"[ac mean] : {sum(amplitude) / len(amplitude):.2f} "
                f"[min amplitude] : {min(amplitude):.2f}",
                f"[max amplitude] : {max(amplitude):.2f}",
                end="\r")

    return sum(amplitude) / len(amplitude), frames


def s30sek_mean(seconds=30, rate=44100, microphone_index=0, p=False):
    audio = pyaudio.PyAudio()
    # Erstellen Sie einen Stream zum Aufnehmen von Audio
    if microphone_index == -1:
        info = audio.get_host_api_info_by_index(0)
        num_devices = info.get('deviceCount')
        print(info)
        # Durchlaufen aller Geräte, um Mikrofone zu finden
        for i in range(0, num_devices):
            if (audio.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
                print("Input Device id ", i, " - ", audio.get_device_info_by_host_api_device_index(0, i).get('name'))
        microphone_index = int(input("Enter Device id :"))
    stream = audio.open(format=pyaudio.paInt16, channels=1,
                        rate=rate, input=True,
                        frames_per_buffer=int(rate / 10), input_device_index=microphone_index)

    mean_amplitude, _ = get_mean_amplitude(stream, seconds=seconds, rate=rate, p=p)

    return mean_amplitude


def get_audio_transcribe(seconds=30,
                         filename=None,
                         model="whisper-1",
                         rate=44100,
                         amplitude_min=82,
                         s_duration_max=1.8,
                         min_speak_duration=1.1, microphone_index=1
                         ):
    if rate <= 0:
        raise ValueError("rate must be bigger then 0 best rate: 44100")
    audio = pyaudio.PyAudio()
    # Erstellen Sie einen Stream zum Aufnehmen von Audio

    if microphone_index == -1:
        info = audio.get_host_api_info_by_index(0)
        num_devices = info.get('deviceCount')
        print(info)
        # Durchlaufen aller Geräte, um Mikrofone zu finden
        for i in range(0, num_devices):
            if (audio.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
                print("Input Device id ", i, " - ", audio.get_device_info_by_host_api_device_index(0, i).get('name'))
        microphone_index = int(input("Enter Device id :"))
    stream = audio.open(format=pyaudio.paInt16, channels=1,
                        rate=rate, input=True,
                        frames_per_buffer=int(rate / 10), input_device_index=microphone_index)

    frames = []
    print(f"Record : Start")

    if filename is None:
        filename = f"{get_app(from_=f'{Name}.get_data_dir').data_dir}/Audio/output.mp3"

    speak_start_time = None
    speak_duration = 0
    silence_duration = 0
    if winsound_init:
        winsound.Beep(320, 125)

    for _ in range(int(rate / int(rate / 10) * seconds)):
        data = stream.read(int(rate / 10))
        frames.append(data)
        audio_np = np.frombuffer(data, dtype=np.int16)
        amplitude = np.abs(audio_np).mean()

        # Check if the amplitude has dropped below a certain threshold
        if amplitude < amplitude_min:
            # If the person has stopped speaking, update the silence duration
            if speak_start_time is not None:
                speak_duration += time.perf_counter() - speak_start_time
                speak_start_time = None
            silence_duration += int(rate / 10) / rate
        else:
            # If the person has started speaking, update the speaking duration
            if speak_start_time is None:
                speak_start_time = time.perf_counter()
                silence_duration = 0
            speak_duration += int(rate / 10) / rate

        if speak_duration != 0 and silence_duration >= s_duration_max:
            break

        if silence_duration >= seconds / 4:
            break

        print(
            f"[speak_duration] : {speak_duration:.2f} [silence_duration] : {silence_duration:.2f} [amplitude] : {amplitude:.2f}",
            end="\r")
        # print(f"[silence_duration] : {silence_duration:.2f}")
        # print(f"[amplitude]        : {amplitude:.2f}")
    if winsound_init:
        winsound.Beep(120, 175)
    stream.stop_stream()
    stream.close()
    audio.terminate()
    print(f"")

    if speak_duration <= min_speak_duration:
        return " "

    print(f"Saving sample")

    filepath = os.path.join(os.getcwd(), filename)
    with wave.open(filepath, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
        wf.setframerate(rate)
        wf.writeframes(
            b''.join(frames))
        wf.close()

    print(f"transcribe sample")

    stream.stop_stream()
    stream.close()
    audio.terminate()

    audio_file = open(filename, "rb")
    res = openai.Audio.translate(model, audio_file)["text"]

    return res


def init_live_transcript(model="jonatasgrosman/wav2vec2-large-xlsr-53-german",
                         rate=16000, chunk_duration=10, amplitude_min=84, microphone_index=1, device=0):
    """
    models EN : 'openai/whisper-tiny'
    DE : 'jonatasgrosman/wav2vec2-large-xlsr-53-german'

    close to live chunk_duration = 1.5
    """
    global PIPLINE
    if PIPLINE is None:
        from transformers import pipeline as PIPLINE
    # Erstelle Queues für die Kommunikation zwischen den Threads und system
    que_t0 = queue.Queue()
    que_t1 = queue.Queue()
    audio_files_que = queue.Queue()
    res_que = queue.Queue()

    def join():
        # Warte bis beide Threads fertig sind
        thread0.join()
        thread1.join()
        os.remove(temp[1]) if os.path.exists(temp[1]) else None
        os.remove(temp[-1]) if os.path.exists(temp[-1]) else None

    def put(x):
        logger.info(
            Style.ITALIC(
                Style.Bold(f"Send data to Threads: {x}")))
        que_t0.put(x)
        que_t1.put(x)

        if x == 'exit':
            join()
            if stream.is_active():
                stream.stop_stream()
            stream.close()
            audio.terminate()

    def pipe_generator():
        def helper_runner(audio_file_name):
            with open(audio_file_name, "rb") as audio_file:
                return openai.Audio.translate(model, audio_file)
        print(f"{torch.cuda.is_available()=}")
        print(f"{torch.cuda.device_count()=}")
        device = 0
        for i_ in range(1, torch.cuda.device_count()):
            print(torch.cuda.get_device_name(i_ - 1))
            device = 1
        if "/" in model:
            return PIPLINE("automatic-speech-recognition", model, device=device)

        elif "-" in model:
            return helper_runner

        else:
            raise ValueError(f"pipe_generator : model is not suppertet : {model}")

    pipe = pipe_generator()

    if rate <= 0:
        raise ValueError("rate must be bigger then 0 best rate: 44100 | 16000")

    audio = pyaudio.PyAudio()
    if microphone_index == -1:
        info = audio.get_host_api_info_by_index(0)
        num_devices = info.get('deviceCount')
        print(info)
        # Durchlaufen aller Geräte, um Mikrofone zu finden
        for i in range(0, num_devices):
            if (audio.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
                print("Input Device id ", i, " - ", audio.get_device_info_by_host_api_device_index(0, i).get('name'))
        microphone_index = int(input("Enter Device id :"))
    # Erstellen Sie einen Stream zum Aufnehmen von Audio
    stream = audio.open(format=pyaudio.paInt16, channels=1,
                        rate=rate, input=True,
                        frames_per_buffer=int(rate / 10), input_device_index=microphone_index)

    logger = get_logger()

    with tempfile.NamedTemporaryFile(suffix=".wav", delete=True) as tf0:
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=True) as tf1:

            temp = 0, tf0.name, tf1.name

            def T0():
                alive = True
                save = False
                frames = []
                logger.info(
                    Style.ITALIC(
                        Style.Bold(
                            f"Record : Start"
                        )))
                chunk_frames = 0
                index = 1
                silence_duration = 0
                speak_duration = 0
                speak_start_time = None
                while alive:

                    if not que_t0.empty():
                        data = que_t0.get()
                        logger.info(
                            Style.ITALIC(
                                Style.Bold(f"T0 Received data : {data}")))
                        if data == 'exit':
                            alive = False
                        if data == 'stop':
                            stream.stop_stream()
                            save = False
                            if winsound_init:
                                winsound.Beep(120, 175)
                        if data == 'start':
                            save = True
                            silence_duration = 0
                            speak_duration = 0
                            speak_start_time = None
                            frames = []
                            stream.start_stream()
                            if winsound_init:
                                winsound.Beep(320, 125)

                    if save:
                        data = stream.read(int(rate / 10))
                        audio_np = np.frombuffer(data, dtype=np.int16)
                        amplitude = np.abs(audio_np).mean()
                        frames.append(data)
                        # Check if the amplitude has dropped below a certain threshold
                        if amplitude < amplitude_min:
                            # If the person has stopped speaking, update the silence duration
                            if speak_start_time is not None:
                                speak_duration += time.perf_counter() - speak_start_time
                                speak_start_time = None
                            silence_duration += int(rate / 10) / rate
                        else:
                            # If the person has started speaking, update the speaking duration
                            if speak_start_time is None:
                                speak_start_time = time.perf_counter()
                            speak_duration += int(rate / 10) / rate
                        print(
                            f"[speak_duration] : {speak_duration:.2f} [silence_duration] : {silence_duration:.2f} [amplitude] : {amplitude:.2f}",
                            end="\r")
                        chunk_frames += 1
                        if chunk_frames >= int(rate / int(rate / 10) * chunk_duration) \
                            and silence_duration > 0.2 \
                            and speak_duration > chunk_duration / 5:
                            # get temp file
                            ac_temp = temp[index]
                            logger.info(
                                Style.ITALIC(
                                    Style.Bold(f"T0 Saving Sample {ac_temp}")))

                            with wave.open(ac_temp, 'wb') as wf:
                                wf.setnchannels(1)
                                wf.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
                                wf.setframerate(rate)
                                wf.writeframes(b''.join(frames))

                            frames = []
                            chunk_frames = 0
                            silence_duration = 0
                            speak_duration = 0
                            speak_start_time = None
                            audio_files_que.put(index)
                            index *= -1

                logger.info(
                    Style.ITALIC(
                        Style.Bold("T0 exiting")))

            def T1():
                alive = True
                transcribe = False
                logger.info(
                    Style.ITALIC(
                        Style.Bold("T1 started")))
                while alive:

                    if not que_t1.empty():
                        data = que_t1.get()
                        logger.info(
                            Style.ITALIC(
                                Style.Bold(f"T1 Received data : {data}")))
                        if data == 'exit':
                            alive = False
                        if data == 'stop':
                            transcribe = False
                        if data == 'start':
                            transcribe = True

                    if transcribe:
                        if not audio_files_que.empty():
                            t0 = time.perf_counter()
                            index = audio_files_que.get()
                            ac_temp = temp[index]
                            logger.info(
                                Style.ITALIC(
                                    Style.Bold(f"T1 Transcribe Sample {ac_temp}")))
                            result = pipe(ac_temp)['text']
                            res_que.put(result)
                            logger.info(
                                Style.ITALIC(
                                    Style.Bold(f"T1 Don in {time.perf_counter() - t0:.3f} chars {len(result)} :"
                                               f" {Style.GREY(result[:10])}..")))

                logger.info(
                    Style.ITALIC(
                        Style.Bold("T1 exiting")))

    thread0 = threading.Thread(target=T0, daemon=True)
    thread1 = threading.Thread(target=T1, daemon=True)

    thread0.start()
    thread1.start()

    return put, res_que
