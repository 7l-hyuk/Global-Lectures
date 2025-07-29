import { LangCode } from "./components";

export interface DubbingRequest {
    video: File
    source_lang: LangCode;
    target_lang: LangCode;
    stt_model: string;
    translation_model: string;
    tts_model: string;
};
