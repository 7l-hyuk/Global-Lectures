from pathlib import Path
import subprocess
import httpx
from pydantic import BaseModel
from src.utils.pipelines.base_stage import PipelineStage
from src.utils.pipelines.tts import TtsClient
from src.utils.audio import AudioSegment


class DubbingPipelineConfig(BaseModel):
    source_lang: str
    target_lang: str
    stt_model: str
    translation_model: str
    tts_model: str
    stt_requset_timeout: float
    translation_requset_timeout: float
    tts_request_timeout: float
    reference_speaker: Path
    tts_output: Path
    dubbing_audio_output: Path
    audio_segments: list[dict] | None = None


class STT(PipelineStage):
    def process(
        self,
        audio_path: Path,
        config: DubbingPipelineConfig
    ):
        payload = {
            "audio_path": str(audio_path),
            "language": config.source_lang,
            "model": config.stt_model
        }
        subtitle = httpx.post(
            "http://localhost:8001/api/v1/stt",
            json=payload,
            timeout=config.stt_requset_timeout
        ).json()
        config.audio_segments = [
            {"start": sub["start"], "end": sub["end"]}
            for sub in subtitle
        ]
        return subtitle, config

class TranslateSubtitle(PipelineStage):
    def process(
        self,
        subtitle: list[dict],
        config: DubbingPipelineConfig
    ):
        payload = {
            "source_lang": config.source_lang,
            "target_lang": config.target_lang,
            "model": config.translation_model,
            "subtitles": subtitle
        }
        translated_subtitle = httpx.post(
            "http://localhost:8002/api/v1/translation",
            json=payload,
            timeout=config.translation_requset_timeout
        ).json()
        return [sub["text"] for sub in translated_subtitle], config
        

class TTS(PipelineStage):
    def process(
        self,
        texts: list[str],
        config: DubbingPipelineConfig
    ):
        tts_client = TtsClient()
        tts_client.run(
            texts=texts,
            target_lang=config.target_lang,
            model=config.tts_model,
            speaker_wav=config.reference_speaker,
            output=config.tts_output,
            timeout=config.tts_request_timeout
        )
        return [config]


class RenderingVideo(PipelineStage):
    def process(
        self,
        config: DubbingPipelineConfig
    ):
        command = ["sox", "-m"]

        for i, sgmt in enumerate(config.audio_segments):
            audio_time = sgmt["end"] - sgmt["start"]
            audio_path = config.tts_output / f"{i:03d}.wav"
            AudioSegment(str(audio_path)).resize(audio_time)
            command.append(f'"|sox {audio_path} -p pad {sgmt["start"]}"')

        temp_output = config.tts_output .with_suffix(".temp.wav")            
        command.append(str(temp_output))
        mix_command = " ".join(command)
        gain_command = f'sox {temp_output} {config.dubbing_audio_output} gain -n'
        subprocess.run(f"{mix_command} && {gain_command} && rm {temp_output}", shell=True)
        
