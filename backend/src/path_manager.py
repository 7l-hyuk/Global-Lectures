import os
import tempfile
from pathlib import Path
import uuid


class UserPath:
    def __init__(self, user_id: uuid.UUID, tmp_dir: str):
        self.user_dir = Path(tmp_dir) / str(user_id)

        self.initilal_video = self.user_dir / "video.mp4"
        self.initilal_audio = self.user_dir / "audio.wav"
    
        self.dubbing_video = self.user_dir / "dubbing.mp4"
        self.dubbing_audio = self.user_dir / "dubbing.wav"

        self.tts_audio_dir = self.user_dir / "dubbing"
        self.tts_audio_sync_dir = self.user_dir / "sync"

        self.source_subtitle = self.user_dir / "source_subtitle.json"
        self.target_subtitle = self.user_dir / "target_subtitle.json"

        bgm_seperation_dir = self.user_dir / "htdemucs" / "audio"
        self.reference_speaker = bgm_seperation_dir / "vocals.wav"
        self.background = bgm_seperation_dir / "no_vocals.wav"

        for dir in [self.tts_audio_dir, self.tts_audio_sync_dir]:
            os.makedirs(dir)
        
if __name__ == "__main__":
    with tempfile.TemporaryDirectory() as tmpdir:
        userpath = UserPath(user_id=uuid.uuid4(), tmp_dir=tmpdir)
        print(userpath.tts_audio_dir)
