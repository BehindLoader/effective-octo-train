import re
from typing import List

import aiohttp

from telegram.client import telegram_client
from telegram.schemas import TelegramWebHookSchema
from constants import REQUEST_HEADERS


class AbstractHandler:
    options = {}

    def __init__(self, message: TelegramWebHookSchema):
        self.message = message

    def _get_user_commands(self) -> List:
        user_commands = []
        if not self.message.message.entities:
            return []
        for entity in (self.message.message.entities):
            if entity.type != 'bot_command':
                continue

            command_text = self.message.message.text[entity.offset:entity.lenght]

            if '@' in command_text:
                at_index = command_text.index('@')
                command_text = command_text[:at_index]

            user_commands.append(
                command_text,
            )
        return user_commands 

    @property
    def can_handle(self) -> bool:
        user_commands = self._get_user_commands()
        commands = self.options.get('commands', [])
        for user_command in user_commands:
            if user_command in commands:
                return True

        for pattern in self.options.get('regexp', []):
            if re.search(
                pattern,
                self.message.message.text,
            ):
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
    error_message = 'Неизвестная команда'

    async def handle(self) -> None:
        if not self.message.message:
            return
        await telegram_client.reply_to(
            self.message.message.chat.id,
            self.message.message.message_id,
            self.error_message,
        )


class TikTokWithUserVideo(AbstractHandler):
    options = {
        'regexp': (
            r'https:\/\/www\.tiktok\.com\/@(.+)\/video\/(\w+)',
        ),
    }

    async def handle(self) -> None:
        # TODO добавить в очередь
        index = self.message.message.text.index('?')
        url = self.message.message.text[:index]
        await telegram_client.reply_to(
            self.message.message.chat.id,
            self.message.message.message_id,
            url,
        )


class TikTokWithoutUserVideo(AbstractHandler):
    options = {
        'regexp': (
            r'^https:\/\/vm\.tiktok\.com\/[\w\d]+\/',
        ),
    }

    async def handle(self) -> None:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                self.message.message.text,
                headers=REQUEST_HEADERS,
            ) as response:
                # TODO добавить в очередь
                url = str(response.url)
                index = url.index('?')
                url = url[:index]
                await telegram_client.reply_to(
                    self.message.message.chat.id,
                    self.message.message.message_id,
                    url,
                )
