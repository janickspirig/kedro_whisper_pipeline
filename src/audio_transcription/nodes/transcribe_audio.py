from pathlib import Path
from typing import Callable, Dict
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


def pri_transcription(
    audio_file_partitions: Dict[str, Callable],
    whisper_params: dict,
) -> Dict[str, str]:
    """Transcribes audio files using OpenAI Whisper.

    Args:
        audio_file_partitions (Dict): Dictionary containing the file names as keys
        and callabale load functions as values.

    Returns:
        Dictionary with the file names as keys and the transcripts as values.
    """

    audios = {
        f_name: load_func() for f_name, load_func in audio_file_partitions.items()
    }

    transcriptions = {}

    client = OpenAI()

    for f_name, audio_data in audios.items():
        transcript = client.audio.transcriptions.create(
            file=Path(audio_data.path), **whisper_params
        )

        transcriptions[f_name] = transcript

    return transcriptions
