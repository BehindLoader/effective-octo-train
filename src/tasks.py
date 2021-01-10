import asyncio
from datetime import datetime, timedelta
from typing import List

import sqlalchemy as sa
from TikTokApi import TikTokApi

from db import db
from models import Message
from settings import settings

api = TikTokApi(use_selenium=True)


async def get_scheduled_messages() -> List[Message]:
    start_of_day = datetime.now().replace(
        hour=0,
        minute=0,
        second=0,
        microsecond=0,
    )
    end_of_day = datetime.now().replace(
        hour=23,
        minute=59,
        second=59,
        microsecond=999999,
    )
    return await db.fetch_all(
        sa.select(
            [Message],
        ).where(
            Message.datetime > start_of_day,
        ).where(
            Message.datetime < end_of_day,
        )
    )


def add_time(old_datetime: datetime) -> datetime:
    new_datetime = old_datetime + timedelta(minutes=30)
    if new_datetime.date() != old_datetime.date():
        return False
    return new_datetime


async def parse_trending(count: int, create_after: datetime) -> None:  # FIXME
    created = 0
    post_datetime = create_after
    for trending in api.trending(count=30):
        post_datetime = add_time(post_datetime)
        if not post_datetime:
            break  # TODO залогировать

        tiktok_url = f'https://www.tiktok.com/@{trending["author"]["uniqueId"]}/video/{trending["id"]}'

        res = await db.fetch_one(
            sa.select(
                [Message],
            ).where(
                Message.url == tiktok_url,
            )
        )
        if res:
            continue  # TODO логировать

        await db.execute(
            sa.insert(
                Message,
            ).values(
                url=tiktok_url,
                status=Message.MessageStatuses.SCHEDULED.value,
                datetime=post_datetime,
                created=datetime.now(),
            )
        )


async def seed_queue() -> None:
    while True:
        scheduled = await get_scheduled_messages()
        if len(scheduled) < settings.PUBLICATIONS_LIMIT_PER_DAY:
            diff = settings.PUBLICATIONS_LIMIT_PER_DAY - len(scheduled)
            max_time = scheduled[-1].get('datetime') if scheduled else datetime.now()
            await parse_trending(diff, max_time)

        await asyncio.sleep(settings.PERIODIC_TASK_COOLDOWN)


async def send_message() -> None:  # TODO FIXME
    while True:
        scheduled = await get_scheduled_messages()
        for message in scheduled:
            from telegram.client import telegram_client
            await telegram_client.send_message(
                -1001450510864,
                message.get('url')
            )

        await asyncio.sleep(60 * 5)

# # downloadAddr

# video = api.trending(count=1)[0]
# print(video)
