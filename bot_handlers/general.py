from typing import Union
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from translations.transtate import with_translation


def general_handlers(dp):
    @dp.message(Command("start"))
    @with_translation
    async def new_connect_handler(message: Message, state: FSMContext, _):
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="🗄️ " + _("Information"), callback_data="info")],
                [InlineKeyboardButton(text="📁 " + _("Parse PDF"), callback_data="parse")],
                [InlineKeyboardButton(text="🗣 " + _("Select your language"), callback_data="language")],
            ]
        )
        await message.answer(_("Welcome! Please choose an option:"), reply_markup=keyboard)

    @dp.message(Command("info"))
    @dp.callback_query(lambda c: c.data == "info")
    @with_translation
    async def show_info(event: Union[Message, CallbackQuery], state: FSMContext, _):
        text = _(
            "Hello! I’m a bot for processing bank statements:\n"
            "    • 📄 I accept a PDF file of your account statement\n"
            "    • 🔎 I analyze the contents and extract transaction data\n"
            "    • 🌐 I allow you to change the interface language via /language\n\n"
            "Send your PDF now to get started!"
        )

        if isinstance(event, CallbackQuery):
            await event.answer()
            target: Message = event.message
        else:
            target = event
        await target.answer(text)

