import logging

from fastapi import APIRouter, HTTPException, Request

from telegram.router import TelegramWebHookHandler
from telegram.schemas import TelegramWebHookSchema

logger = logging.getLogger('TelegramWebHook')
router = APIRouter()


@router.post('/webhook')
async def receive_webhook(item: TelegramWebHookSchema, req: Request):
    logger.debug(await req.body())

    handler = TelegramWebHookHandler(item)
    await handler.process()
