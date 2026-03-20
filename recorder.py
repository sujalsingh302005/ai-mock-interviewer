import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import os
import threading

SAMPLE_RATE = 16000
AUDIO_FILE = "temp_answer.wav"

_recording = False
_frames = []
_thread = None

def _record_worker(max_duration):
    global _recording, _frames
    _frames = []
    chunk_size = 1024
    max_chunks = int(SAMPLE_RATE * max_duration / chunk_size)

    with sd.InputStream(samplerate=SAMPLE_RATE, channels=1, dtype='int16', blocksize=chunk_size) as stream:
        for _ in range(max_chunks):
            if not _recording:
                break
            data, _ = stream.read(chunk_size)
            _frames.append(data.copy())

def start_recording(max_duration=60):
    global _recording, _thread
    _recording = True
    _thread = threading.Thread(target=_record_worker, args=(max_duration,), daemon=True)
    _thread.start()

def stop_recording():
    global _recording, _thread, _frames
    _recording = False
    if _thread:
        _thread.join(timeout=2)
    if _frames:
        audio = np.concatenate(_frames, axis=0)
        wav.write(AUDIO_FILE, SAMPLE_RATE, audio)
        return AUDIO_FILE
    return None

def is_recording():
    return _recording

def cleanup():
    if os.path.exists(AUDIO_FILE):
        os.remove(AUDIO_FILE)
