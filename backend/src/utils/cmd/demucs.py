from src.utils.path import UserPath

DEMUCS = "demucs"

def seperate_vocal(user_path: UserPath):
    return [
        DEMUCS,
        "--two-stems=vocals",
        "-o", user_path.user,
        user_path.reference_speaker
    ]
