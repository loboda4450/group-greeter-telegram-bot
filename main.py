import asyncio
import logging

import yaml

from telethon import TelegramClient, events
from telethon.tl.types import User


def get_sender_name(sender: User) -> str:
    if sender.username:
        return "" + sender.username
    elif sender.first_name and sender.last_name:
        return "{} {}".format(sender.first_name, sender.last_name)
    elif sender.first_name:
        return sender.first_name
    elif sender.last_name:
        return sender.last_name
    else:
        return "PersonWithNoName"


async def main(config):
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=config['log_level'])
    logger = logging.getLogger(__name__)
    client = TelegramClient(**config['telethon_settings'])
    print("Starting")

    if not config['bot_token']:
        raise Exception('No bot token provided')

    await client.start(bot_token=config['bot_token'])
    print("Started")

    @client.on(event=events.ChatAction())
    async def status(event):
        if event.user_added or event.user_joined:
            await event.reply(f"Witaj na grupce [{get_sender_name(event.user)}](tg://user?id={event.user.id}) ,"
                              f" przeczytaj przypięty post i ciesz się z pobytu.\n\nA, i coś w gratisie:")
            await event.reply("https://www.deezer.com/track/1357553832")

    async with client:
        print("Good morning!")
        await client.run_until_disconnected()


if __name__ == '__main__':
    with open("config.yml", 'r') as f:
        config = yaml.safe_load(f)
        asyncio.get_event_loop().run_until_complete(main(config=config))
