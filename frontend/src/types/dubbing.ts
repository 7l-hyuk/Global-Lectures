export interface DubbingRequest {
    video: File
    source_lang: string;
    target_lang: string;
    stt_model: string;
    translation_model: string;
    tts_model: string;
};
