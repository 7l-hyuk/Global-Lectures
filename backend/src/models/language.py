from dataclasses import dataclass


@dataclass
class SupportedLanguages:
    CODE = {
        "Korean": "ko",
        "English": "en",
        "Japanese": "ja",
        "Chinese": "zh"
    }
    WHISPERX = {
        "ko": "ko",
        "en": "en",
        "ja": "ja",
        "zh": "zh"
    }
    NLLB = {
        "ko": "kor_Hang",
        "en": "eng_Latn",
        "ja": "jpn_Jpan",
        "zh": "zho_Hans"
    }
    XTTS_V2 = {
        "ko": "ko",
        "en": "en",
        "ja": "ja",
        "zh": "zh"
    }
