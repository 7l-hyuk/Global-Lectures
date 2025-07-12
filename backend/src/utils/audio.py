import os
from dataclasses import dataclass
import subprocess
import soundfile as sf
import src.utils.cmd.sox as sox


@dataclass
class AudioSegment:
    path: str

    @property
    def time(self):
        f = sf.SoundFile(self.path)
        return len(f) / f.samplerate       

    def resize(self, time: float):
        temp_path = self.path + ".tmp.wav"
        cmd = sox.resize(
            wav_path=self.path,
            output_path=temp_path,
            speed=self.time / time
        )
        subprocess.run(cmd, check=True)
        os.replace(temp_path, self.path)
