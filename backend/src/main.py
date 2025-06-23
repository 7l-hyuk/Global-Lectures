from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.routes.auth import auth_router


app = FastAPI()

origins = [
    "*"
]
routes = [
    auth_router
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

for router in routes:
    app.include_router(router)
