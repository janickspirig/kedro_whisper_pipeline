from typing import Callable, Dict
from noisereduce.torchgate import TorchGate as TG
from audio_transcription.datasets.audio_dataset import AudioData


def int_noise_reduction(
    audio_file_partitions: Dict[str, Callable],
) -> Dict[str, AudioData]:
    """Reduces noise in wave audios.

    Args:
        audio_file_partitions (Dict): Dictionary containing the file names as keys and callabale load functions as values.

    Returns:
        Dictionary with the file names as keys and the noise reduced data as values.
    """
    audios = {
        f_name: load_func() for f_name, load_func in audio_file_partitions.items()
    }

    for f_name, audio_data in audios.items():
        tg = TG(sr=audio_data.sample_rate, nonstationary=True)

        audio_w_noise = audio_data.waves
        audio_no_noise = tg(audio_w_noise)
        audio_data.waves = audio_no_noise

        audios[f_name] = audio_data

    return audios
