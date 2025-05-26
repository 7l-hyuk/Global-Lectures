import os
from pathlib import Path
import uuid


class UserPath:
    def __init__(self, user_id: uuid.UUID):
        self.user = Path("data") / str(user_id)

        self.original_video = self.user / "original_video.mp4"
        self.reference_speaker = self.user / "reference_speaker.wav"
        self.dub_audio = self.user / "dub.wav"
        self.dub_video = self.user / "dub.mp4"
        self.tts_audio = self.user / "tts_audio"
        self.tts_audio_sync = self.user / "tts_audio_sync"

        for dir in [self.user, self.tts_audio, self.tts_audio_sync]:
            os.makedirs(dir, exist_ok=True)


if __name__ == "__main__":
    userpath = UserPath(uuid.uuid4())
    print(userpath.tts_audio_sync)
