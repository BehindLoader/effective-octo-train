import asyncio
import logging

import uvicorn
from fastapi import FastAPI

from db import db
from settings import settings
from tasks import seed_queue, send_message
from telegram.views import router as telegram_router

app = FastAPI()

app.include_router(telegram_router)


@app.on_event('startup')
async def on_startup_event():
    await db.connect()
    asyncio.create_task(seed_queue())
    asyncio.create_task(send_message())


if __name__ == "__main__":
    uvicorn.run(
        'app:app',
        reload=settings.UVICORN_RELOAD,
        reload_dirs=['src'],
        debug=settings.UVICORN_DEBUG,
        log_config=settings.LOGGING,
        log_level=settings.UVICORN_LOG_LEVEL,
    )
