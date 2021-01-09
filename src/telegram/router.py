from telegram.handlers import HelpHandler, NotFoundHandler, StartHandler
from telegram.schemas import TelegramWebHookSchema

HANDLERS = [
    HelpHandler,
    StartHandler,
]


class TelegramWebHookHandler:
    def __init__(self, message: TelegramWebHookSchema):
        self.message = message

    async def process(self) -> None:
        for Handler in HANDLERS:
            handler = Handler(self.message)
            if handler.can_handle:
                await handler.handle()
                break
        else:
            await NotFoundHandler(self.message).handle()
