from telegram.handlers import (HelpHandler, NotFoundHandler, StartHandler,
                               TikTokWithoutUserVideo, TikTokWithUserVideo)
from telegram.schemas import TelegramWebHookSchema

HANDLERS = [
    HelpHandler,
    StartHandler,
    TikTokWithUserVideo,
    TikTokWithoutUserVideo,
]


class TelegramWebHookHandler:
    def __init__(self, message: TelegramWebHookSchema):
        self.message = message

    async def process(self) -> None:
        for Handler in HANDLERS:
            handler = Handler(self.message)
            try:
                can_handle = handler.can_handle
            except Exception as exc:
                can_handle = False
                pass  # TODO добавить логирование
            else:
                if can_handle:
                    await handler.handle()
                    break
        else:
            await NotFoundHandler(self.message).handle()
