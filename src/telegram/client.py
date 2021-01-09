import logging
from typing import Dict

import aiohttp
from settings import settings

logger = logging.getLogger('TelegramClient')


class TelegramClientError(Exception):
    """Telegram API Error."""


class TelegramAPIClient:
    # TODO добавить полей, новых команд

    def __init__(self, api_token: str):
        self.api_token = api_token

    def _make_url(self, command: str) -> str:
        return f'https://api.telegram.org/bot{self.api_token}/{command}'

    async def _request(
        self,
        command: str,
        options: Dict,
    ) -> Dict:
        url = self._make_url(command)
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=options) as response:
                response.raise_for_status()
                return await response.json()

    async def request(
        self,
        command: str,
        options: Dict,
    ) -> Dict:
        try:
            await self._request(
                command = command,
                options = options,
            )
        except aiohttp.ClientError as exc:
            logger.error(f'Telegram API Error with {command}: {exc}')
            raise TelegramClientError()

    async def send_message(
        self,
        chat_id: int,
        text: str,
    ):
        return await self.request(
            'sendMessage',
            {
                'chat_id': chat_id,
                'text': text,
            }
        )

    async def reply_to(
        self,
        chat_id: int,
        message_id: int,
        text: str,
    ):
        return await self.request(
            'sendMessage',
            {
                'chat_id': chat_id,
                'text': text,
                'reply_to_message_id': message_id,
            }
        )


telegram_client = TelegramAPIClient(settings.TELEGRAM_BOT_TOKEN)
