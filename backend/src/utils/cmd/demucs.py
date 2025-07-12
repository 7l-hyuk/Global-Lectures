DEMUCS = "demucs"

def seperate_bgm(output: str, wav_path: str):
    return [
        DEMUCS,
        "--two-stems=vocals",
        "-o", output,
        wav_path
    ]
