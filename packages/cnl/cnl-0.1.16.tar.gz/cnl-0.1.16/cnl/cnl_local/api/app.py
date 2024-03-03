from fastapi import FastAPI

from cnl_local.api.controllers.datasets_samples import router as datasets_samples_router
from cnl_local.api.controllers.logged_conversations import (
    router as logged_conversations_router,
)

app = FastAPI()

app.include_router(datasets_samples_router)
app.include_router(logged_conversations_router)


# Allow all cors for dev purposes
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
