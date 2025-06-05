from fastapi import APIRouter
from fastapi.responses import FileResponse
from src.schema.analysis import Subtitle

analysis_router = APIRouter(prefix="/api/analysis", tags=["Subtitle Analysis"])


@analysis_router.get("/")
def subtitle_analysis(subtitle: list[Subtitle]):
    # TODO: 대본을 받아서 워드클라우드를 return
    return FileResponse(...)