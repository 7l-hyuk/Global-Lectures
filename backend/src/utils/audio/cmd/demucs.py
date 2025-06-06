from src.utils.path import UserPath

DEMUCS = "demucs"

def seperate_vocal(userpath: UserPath):
    return [
        DEMUCS,
        "--two-stems=vocals",
        "-o", userpath.user,
        userpath.reference_speaker
    ]
