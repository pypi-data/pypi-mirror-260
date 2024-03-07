import wave

import numpy as np


def sample_wav(file_path: str):
    """
    Sampling a .wav file

    :param file_path:  The absolute path to the .wav file to be sampled

    :return: an array of sampled points
    """
    with wave.open(file_path, "rb") as f:
        frames = f.readframes(f.getnframes())
        return np.frombuffer(frames, dtype=np.int16)
