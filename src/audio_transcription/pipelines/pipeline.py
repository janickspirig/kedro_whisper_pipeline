from kedro.pipeline import Pipeline, node

from audio_transcription.nodes.reduce_noise import int_noise_reduction
from audio_transcription.nodes.transcribe_audio import pri_transcription


def create_pipeline(**kwargs):
    return Pipeline(
        nodes=[
            node(
                int_noise_reduction,
                inputs=[
                    "raw_audio_files",
                ],
                outputs="mi_audio_files",
                name="reduce_noise",
            ),
            node(
                pri_transcription,
                inputs=[
                    "mi_audio_files",
                    "params:whisper_api_kwargs",
                ],
                outputs="mo_transcripts",
                name="transcribe",
            ),
        ],
    )
