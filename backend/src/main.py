from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.routes.users import users_router
from src.routes.dub import dubbing_router

app = FastAPI()

origins = [
    "http://localhost:3000",  # React 개발 서버 주소
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users_router)
app.include_router(dubbing_router)