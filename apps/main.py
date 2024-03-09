from typing import Union

from fastapi import FastAPI
from apps.conf import get_settings

from apps.auth.views import router as auth_router
from apps.fit.views import router as home_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

SETTINGS = get_settings()
app.include_router(auth_router, prefix=SETTINGS.API_PREFIX)
app.include_router(home_router, prefix=SETTINGS.API_PREFIX)
origins = [
    "http://localhost:8000"  # TODO: make it dynamic with encironment variable
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
