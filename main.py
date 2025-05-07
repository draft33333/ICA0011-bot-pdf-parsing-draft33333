import os
import sys
import asyncio
import logging
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.types import BotCommandScopeDefault
from aiogram.client.default import DefaultBotProperties

from bot_handlers.change_language import language_handlers
from bot_handlers.general import general_handlers
from bot_handlers.parser import parse_handlers
from translations.transtate import LANGUAGES, get_translator

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

dp = Dispatcher()
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))


def get_bot_commands(_):
    """Return a list of localized bot commands"""
    return [
        types.BotCommand(command="/info", description=_("Information about the bot")),
        types.BotCommand(command="/parse", description=_("Parse PDF")),
        types.BotCommand(command="/language", description=_("Select your language")),
    ]


async def set_bot_commands():
    """ Bot command's buttons """
    for lang in LANGUAGES:
        _ = get_translator(lang)
        commands = get_bot_commands(_)
        await bot.set_my_commands(commands, scope=BotCommandScopeDefault(), language_code=lang)


# /start   /info
general_handlers(dp)

# /parse
parse_handlers(dp)

# /language
language_handlers(dp)


async def main() -> None:
    await set_bot_commands()
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
