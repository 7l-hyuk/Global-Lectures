from src.utils.pipelines.setup_stages import (
    DownloadVideo,
    ExtractAudio,
    SeperateBGMFromAudio,
    RemoveVocalsFromVideo,
    ExtractReferenceSpeaker
)
from src.utils.pipelines.dubbing_stages import STT, TranslateSubtitle, TTS, RenderingVideo
from src.utils.pipelines.pipeline import Pipeline


def get_setup_pipeline():
    return Pipeline(
        [
            DownloadVideo(),
            ExtractAudio(),
            SeperateBGMFromAudio(),
            RemoveVocalsFromVideo(),
            ExtractReferenceSpeaker()
        ]
    )


def get_dubbing_pipeline():
    return Pipeline(
        [
            STT(),
            TranslateSubtitle(),
            TTS(),
            RenderingVideo()
        ]
    )
