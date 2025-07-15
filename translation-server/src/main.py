import time

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.schema import SubtitleEntry, TranslationModelConfig
from src.models.tanslator import translation_service

app = FastAPI()
app.add_middleware(
   CORSMiddleware,
    allow_origins=["http://localhost:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/api/v1/translation", response_model=list[SubtitleEntry])
def subtitle_translate(
    model_config: TranslationModelConfig,
):
    start = time.time()
    translator = translation_service.create_service(
        name="NLLB-200",
        source_lang=model_config.source_lang,
        target_lang=model_config.target_lang
    )
    subtitle = translator.run(model_config.subtitles)
    print(f"Processed In {time.time() - start} s")
    return subtitle
