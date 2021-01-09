import logging

import uvicorn
from fastapi import FastAPI

from settings import settings
from telegram.views import router as telegram_router

app = FastAPI()

app.include_router(telegram_router)


if __name__ == "__main__":
    uvicorn.run(
        'app:app',
        reload=settings.UVICORN_RELOAD,
        reload_dirs=['src'],
        debug=settings.UVICORN_DEBUG,
        log_config=settings.LOGGING,
        log_level=settings.UVICORN_LOG_LEVEL,
    )
