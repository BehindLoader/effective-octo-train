from typing import List

from telegram.client import telegram_client
from telegram.schemas import TelegramWebHookSchema


class AbstractHandler:
    options = {}

    def __init__(self, message: TelegramWebHookSchema):
        self.message = message

    def _get_user_commands(self) -> List:  # TODO обрезать все после @
        user_commands = []
        if not self.message.message.entities:
            return []
        for entity in (self.message.message.entities):
            if entity.type != 'bot_command':
                continue

            user_commands.append(
                self.message.message.text[entity.offset:entity.lenght],
            )
        return user_commands 

    @property
    def can_handle(self) -> bool:
        user_commands = self._get_user_commands()
        commands = self.options.get('commands', [])
        for user_command in user_commands:
            if user_command in commands:
                return True

        

        return False

    async def handle(self) -> None:
        raise NotImplementedError()


class HelpHandler(AbstractHandler):
    options = {
        'commands': ['/help'],
    }
    help_message = 'help'

    async def handle(self) -> None:
        await telegram_client.send_message(
            self.message.message.chat.id,
            self.help_message,
        )


class StartHandler(HelpHandler):
    options = {
        'commands': ['/start'],
    }
    help_message = 'start'


class NotFoundHandler(AbstractHandler):
    options = {
        'echo': True,
    }
    error_message = 'Неизвестная команда'

    async def handle(self) -> None:
        await telegram_client.reply_to(
            self.message.message.chat.id,
            self.message.message.message_id,
            self.error_message,
        )
