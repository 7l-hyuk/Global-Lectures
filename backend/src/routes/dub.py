import uuid
import shutil
from fastapi import APIRouter, UploadFile, Form
from fastapi.responses import FileResponse


from src.utils.path import UserPath
import src.services.dub as service
from src.models.language import SupportedLanguages

dubbing_router = APIRouter(prefix="/v1/dub", tags=["dub service"])


@dubbing_router.post("/")
async def get_dub_video(
    video: UploadFile,
    source_lang: str = Form(..., alias="sourceLang"),
    target_lang: str = Form(..., alias="targetLang")
):
    source_lang = SupportedLanguages.CODE[source_lang]
    target_lang = SupportedLanguages.CODE[target_lang]
    userpath = UserPath(uuid.uuid4())

    with open(userpath.original_video, "wb") as f:
        shutil.copyfileobj(video.file, f)

    service.dub(
        userpath=userpath,
        src_lang=source_lang,
        tar_lang=target_lang
    )

    output = userpath.dub_video
    return FileResponse(
        output,
        media_type="video/mp4",
        filename=output.name
    )
