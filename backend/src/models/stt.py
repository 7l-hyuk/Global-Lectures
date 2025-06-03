import requests

import whisperx

from src.models.basemodel import BaseServiceModel, device
from src.models.registry import register_service
from src.config import service_settings


@register_service("stt")
class STTServiceModel(BaseServiceModel):
    def init_model(self):
        self.model = whisperx.load_model(
            whisper_arch="large-v2",
            device=device,
            compute_type="float16" if device == "cuda" else "int8"
        )
        self.aligned_model, self.metadata = whisperx.load_align_model(
            language_code=self.language[0],
            device=device
        )

    def process(self):
        audio = str(self.userpath.reference_speaker)
        segments = self.model.transcribe(audio, language=self.language[0])["segments"]
        aligned: dict[str, dict] = whisperx.align(
            segments,
            self.aligned_model,
            self.metadata,
            audio,
            device
        )
        return aligned["segments"]


@register_service("stt-elevenlabs")
class ElevenlabsSTTServiceModel(BaseServiceModel):
    def init_model(self):
        self.API_URL = "https://api.elevenlabs.io//v1/speech-to-text"
        self.files = {
            'file': open(str(self.userpath.reference_speaker), 'rb')
        }
        self.data = {
            "model_id": "scribe_v1",
            "language_code": "ko",
            "diarize": False  # 스피커 분리 필요 없으면 False
        }
        self.headers = {
            "xi-api-key": service_settings.XI_API_KEY
        }


    def process(self):
        def _is_end(word: str):
            if word[-1] in [".", "!", "?"]:
                return True
            return False

        response = requests.post(
            self.API_URL,
            headers=self.headers,
            files=self.files,
            data=self.data
        )
        result: dict = response.json()
        words = result.get("words")

        sentence = ""
        subtitle: list[dict] = []

        for word in words:
            text = word["text"]

            if not sentence:
                start = word["start"]
            
            sentence += text
            
            if _is_end(text):
                end = word["end"]
                subtitle.append(
                    {
                        "text": sentence,
                        "start": start,
                        "end": end
                    }
                )
                sentence = ""
        print(subtitle)
        return subtitle
    




    


    
    
