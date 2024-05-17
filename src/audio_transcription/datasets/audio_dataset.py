from pathlib import PurePosixPath
from typing import Any, Dict


from pydantic import BaseModel
import torch

import fsspec
import numpy as np
import torchaudio
from kedro.io import AbstractDataset
from kedro.io.core import get_filepath_str, get_protocol_and_path


class AudioData(BaseModel):
    path: str
    waves: Any  # torch.Tensor
    sample_rate: int


class AudioDataset(AbstractDataset[torch.Tensor, torch.Tensor]):
    """AudioDataset class to load an audio file using torchaudio."""

    def __init__(self, filepath: str):
        """Creates a new instance of AudioDataset to load / save image data at the given filepath.

        Args:
            filepath: The location of the image file to load / save data.
        """
        protocol, path = get_protocol_and_path(filepath)

        self._protocol = protocol
        self._filepath = PurePosixPath(path)
        self._fs = fsspec.filesystem(self._protocol)

    def _load(self) -> AudioData:
        """Loads data from an .mp3 audio file.

        Returns:
            AudioData object containing the data of the audio file.
        """
        load_path = get_filepath_str(self._filepath, self._protocol)
        with self._fs.open(load_path) as f:
            audio, sample_rate = torchaudio.load(uri=load_path, channels_first=True)
            return AudioData(path=load_path, waves=audio, sample_rate=sample_rate)

    def _save(self, audio: AudioData) -> None:
        """Saves audio file back to specified filepath.

        Args:
            audio (AudioData): The audio object to be saved.
        """
        save_path = get_filepath_str(self._filepath, self._protocol)
        with self._fs.open(save_path, "wb") as f:
            torchaudio.save(
                uri=save_path, src=audio.waves, sample_rate=audio.sample_rate
            )

    def _describe(self) -> Dict[str, Any]:
        """Returns a dict that describes the attributes of the dataset"""
        ...
